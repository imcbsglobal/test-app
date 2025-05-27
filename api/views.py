# api/views.py
import logging
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from datetime import datetime, timedelta
from django.conf import settings
from .models import AdminCredential, AccInvDetails, AccInvMast, AccProduct, AccProduction, AccProductionDetails, AccPurchaseDetails, AccPurchaseMaster
from .serializers import AdminCredentialSerializer, AccInvDetailsSerializer, AccInvMastSerializer, AccProductSerializer, AccProductionDetailsSerializer, AccPurchaseDetailsSerializer, AccPurchaseMasterSerializer
from django.contrib.auth.hashers import check_password
import jwt
from django.db.models import Q, Sum
from django.utils.dateparse import parse_date
from .permissions import IsAdminAuthenticated

logger = logging.getLogger(__name__)

# INDEX VIEW
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# HOME VIEW
class HomeView(APIView):
    def get(self, request):
        #return Response({"message": "Welcome to the Omega-Backend API"})
        return render(request, 'home.html')

# LOGIN VIEW
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = AdminCredential.objects.get(username=username)
        except AdminCredential.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.password != password:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=365),  # Token valid for 1 year
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token})
    

# LOGOUT VIEW
class LogoutView(APIView):
    def post(self, request):
        # In a real JWT system, you can't "invalidate" the token server-side unless you store a blacklist.
        # This is just a dummy response to indicate a successful logout.
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    
# STOCK REPORT PAGE RENDERING VIEW
class StockReportView(View):
    def get(self, request):
        return render(request, 'StockReport.html')
    
# TRANSACTION DETAILS PAGE RENDERING VIEW
class TransactionDetailsView(View):
    def get(self, request):
        return render(request, 'TransactionDetails.html')


# ===== API ENDPOINTS FOR PRODUCTS =====

## StockReport.html page API views
class ProductListAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]
    """
    Get all products with optional filtering
    GET /api/products/?stockCategory=value&brand=value&search=value&product=value
    """
    def get(self, request):
        try:
            # Get filter parameters
            stock_category = request.GET.get('stockCategory')
            brand = request.GET.get('brand')
            product = request.GET.get('product')  # Added product filter
            search = request.GET.get('search')

            logger.debug(f"Filtering with stockCategory={stock_category}, brand={brand}, product={product}, search={search}")
            
            # Start with all products
            queryset = AccProduct.objects.all()
            
            # Apply filters
            if stock_category and stock_category != 'all':
                queryset = queryset.filter(stockcatagory=stock_category)
            
            if brand and brand != 'all':
                queryset = queryset.filter(brand=brand)
            
            if product and product != 'all':
                queryset = queryset.filter(product=product)
            
            # Apply search filter
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | 
                    Q(code__icontains=search) |
                    Q(product__icontains=search) |
                    Q(brand__icontains=search) |
                    Q(stockcatagory__icontains=search)
                )
            
            # Order by name for consistent display
            queryset = queryset.order_by('name')
            
            # Serialize the data
            serializer = AccProductSerializer(queryset, many=True)
            
            # Ensure unit field is properly formatted
            formatted_data = []
            for item in serializer.data:
                # Format unit field to show [UNIT] format if needed
                unit = item.get('unit', '')
                if unit and not unit.startswith('['):
                    unit = f"[{unit}]"
                
                formatted_item = {
                    **item,
                    'unit': unit,
                    # Ensure billedcost is properly formatted
                    'billedcost': float(item.get('billedcost', 0)) if item.get('billedcost') else 0.00,
                    'quantity': int(float(item.get('quantity', 0))) if item.get('quantity') else 0
                }
                formatted_data.append(formatted_item)
            
            logger.info(f"Returned {len(formatted_data)} products")
            return Response({
                'success': True,
                'data': formatted_data,
                'count': len(formatted_data)
            })
            
        except Exception as e:
            logger.error(f"Error in ProductListAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockCategoriesAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]
    """
    Get all unique stock categories
    GET /api/stock-categories/
    """
    def get(self, request):
        try:
            categories = AccProduct.objects.filter(
                stockcatagory__isnull=False,
                stockcatagory__gt=''  # Exclude empty strings
            ).values_list('stockcatagory', flat=True).distinct().order_by('stockcatagory')

            logger.info(f"Found {len(categories)} unique stock categories.")
            
            return Response({
                'success': True,
                'data': list(categories)
            })

        except Exception as e:
            logger.error(f"Error in StockCategoriesAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrandsAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]
    """
    Get all unique brands
    GET /api/brands/
    """
    def get(self, request):
        try:
            brands = AccProduct.objects.filter(
                brand__isnull=False,
                brand__gt=''  # Exclude empty strings
            ).values_list('brand', flat=True).distinct().order_by('brand')

            logger.info(f"Found {len(brands)} unique brands.")
            
            return Response({
                'success': True,
                'data': list(brands)
            })
            
        except Exception as e:
            logger.error(f"Error in BrandsAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]
    """
    Get all unique product names
    GET /api/products-list/
    """
    def get(self, request):
        try:
            products = AccProduct.objects.filter(
                product__isnull=False,
                product__gt=''  # Exclude empty strings
            ).values_list('product', flat=True).distinct().order_by('product')

            logger.info(f"Found {len(products)} unique products.")
            
            return Response({
                'success': True,
                'data': list(products)
            })
            
        except Exception as e:
            logger.error(f"Error in ProductsAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]
    """
    Get product by code
    GET /api/products/{code}/
    """
    def get(self, request, code):
        try:
            product = AccProduct.objects.get(code=code)
            serializer = AccProductSerializer(product)

            # Format the response data
            product_data = serializer.data
            unit = product_data.get('unit', '')
            if unit and not unit.startswith('['):
                unit = f"[{unit}]"
            
            product_data['unit'] = unit
            product_data['billedcost'] = float(product_data.get('billedcost', 0)) if product_data.get('billedcost') else 0.00

            logger.info(f"Product found with code {code}")
            
            return Response({
                'success': True,
                'data': product_data
            })
            
        except AccProduct.DoesNotExist:
            logger.warning(f"Product not found with code {code}")
            return Response({
                'success': False,
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Error in ProductDetailAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

## TransactionDetails.html page API views
class ProductSummaryAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]

    def get(self, request):
        try:
            # Get filters
            stock_category = request.GET.get('stockCategory')
            brand = request.GET.get('brand')
            product = request.GET.get('product')
            search = request.GET.get('search')

            queryset = AccProduct.objects.all()

            if stock_category and stock_category != 'all':
                queryset = queryset.filter(stockcatagory=stock_category)

            if brand and brand != 'all':
                queryset = queryset.filter(brand=brand)

            if product and product != 'all':
                queryset = queryset.filter(product=product)

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(code__icontains=search) |
                    Q(product__icontains=search) |
                    Q(brand__icontains=search) |
                    Q(stockcatagory__icontains=search)
                )

            queryset = queryset.order_by('name')

            # Get list of codes from filtered products
            product_codes = list(queryset.values_list('code', flat=True))

            # Bulk pre-fetch and sum quantities by code
            inv_qs = AccInvDetails.objects.filter(code__in=product_codes).values('code').annotate(total=Sum('quantity'))
            purchase_qs = AccPurchaseDetails.objects.filter(code__in=product_codes).values('code').annotate(total=Sum('quantity'))
            production_qs = AccProductionDetails.objects.filter(code__in=product_codes).values('code').annotate(total=Sum('qty'))

            # Build fast lookup dicts
            inv_map = {item['code']: item['total'] or 0 for item in inv_qs}
            purchase_map = {item['code']: item['total'] or 0 for item in purchase_qs}
            production_map = {item['code']: item['total'] or 0 for item in production_qs}

            summary_data = []

            for product in queryset:
                code = product.code
                summary_data.append({
                    'code': code,
                    'name': product.name,
                    'inv_quantity': int(inv_map.get(code, 0)),
                    'purchase_quantity': int(purchase_map.get(code, 0)),
                    'production_quantity': int(production_map.get(code, 0)),
                })

            return Response({
                'success': True,
                'data': summary_data,
                'count': len(summary_data)
            })

        except Exception as e:
            logger.error(f"Error in ProductSummaryAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Product summary by date API View
class ProductSummaryByDateAPIView(APIView):
    permission_classes = [IsAdminAuthenticated]

    def get(self, request):
        try:
            from_date = request.GET.get('fromDate')
            to_date = request.GET.get('toDate')

            if not from_date or not to_date:
                return Response({
                    'success': False,
                    'error': 'fromDate and toDate are required.'
                }, status=status.HTTP_400_BAD_REQUEST)

            from_date = parse_date(from_date)
            to_date = parse_date(to_date)

            # --- SALES (INVENTORY) ---
            inv_slnos = AccInvMast.objects.filter(invdate__range=(from_date, to_date)).values_list('slno', flat=True)
            inv_qs = AccInvDetails.objects.filter(invno__in=inv_slnos)
            inv_data = inv_qs.values('code').annotate(total=Sum('quantity'))
            sales_map = {item['code']: item['total'] or 0 for item in inv_data}

            # --- PURCHASE ---
            purchase_slnos = AccPurchaseMaster.objects.filter(date__range=(from_date, to_date)).values_list('slno', flat=True)
            purchase_qs = AccPurchaseDetails.objects.filter(billno__in=purchase_slnos)
            purchase_data = purchase_qs.values('code').annotate(total=Sum('quantity'))
            purchase_map = {item['code']: item['total'] or 0 for item in purchase_data}

            # --- PRODUCTION ---
            production_nos = AccProduction.objects.filter(date__range=(from_date, to_date)).values_list('productionno', flat=True)
            production_qs = AccProductionDetails.objects.filter(masterno__in=production_nos)
            production_data = production_qs.values('code').annotate(total=Sum('qty'))
            production_map = {item['code']: item['total'] or 0 for item in production_data}

            # --- ALL PRODUCTS ---
            product_qs = AccProduct.objects.values('code', 'name')
            code_name_map = {item['code']: item['name'] for item in product_qs}
            all_codes = set(code_name_map.keys())  # show all products, not just involved ones

            # --- FINAL RESULT ---
            summary_data = []
            for code in all_codes:
                summary_data.append({
                    'code': code,
                    'name': code_name_map.get(code, 'Unknown Product'),
                    'sales_quantity': float(sales_map.get(code, 0)),
                    'purchase_quantity': float(purchase_map.get(code, 0)),
                    'production_quantity': float(production_map.get(code, 0)),
                })

            return Response({
                'success': True,
                'data': summary_data,
                'count': len(summary_data)
            })

        except Exception as e:
            logger.error(f"Error in ProductSummaryByDateAPIView: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)