import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet): # هذا الكلاس راح نستدعيه في الفيو
    #هنا احط الفلتر كيف ابغاه يكون
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="name", lookup_expr="icontains")#هنا راح يسوي فلتر على حسب اللي يدخله , الاتربيوت الاول يعني راح يبحث في كولم الاسم,الاتربيوت الثاني يعني على حسب المدخل اي محتوى مو شرط يكون بالضبط مثلا لو دخلت بس حرفين راح يطلع النتايج عادي
    minPrice = django_filters.filters.NumberFilter(field_name="price" or 0, lookup_expr="gte")#لو مثلا المدخل كان الف فيرجع اقل شيءالف يعني اكبر من او يساوي
    maxPrice = django_filters.filters.NumberFilter(field_name="price" or 10000, lookup_expr="lte")#اقل من او يساوي
    class Meta:
        model = Product
        #fields = ['category', 'brand', 'price'] #نحدد الفلتر يكون على حسب ايش
        fields = ('category', 'brand', 'keyword','minPrice','maxPrice')