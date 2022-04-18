
# method 1
class GetVariantMetaDataUsingHGVScDNA(viewsets.ModelViewSet):
 """ViewSet for the GetVariantMetaDataUsingHGVScDNA class"""
 
    #models.Variant_Transcript.objects.filter(hgvs_cdna='NM_000059.4:c.68_69delAG' )
    queryset = models.Variant_Transcript.objects.all()
    serializer_class = serializers.VariantMetaDataSerializer
    lookup_field = 'hgvs_cdna'
    lookup_value_regex = "NM.+" #"[^/]+" , 'NM_\d+.\d+:.+' , '.+'
    permission_classes = [permissions.IsAuthenticated]


 # method 2
from rest_framework.response import Response

class GetVariantMetaDataUsingHGVScDNA(viewsets.ModelViewSet):
    
      #queryset = ''
      lookup_value_regex =  '.+'
      serializer_class = serializers.VariantMetaDataSerializer

      def get_queryset(self):
          return models.Variant_Transcript.objects.all()

      def retrieve(self, request, *args, **kwargs):
        
        params = kwargs
        print(params)

        response = models.Variant_Transcript.objects.filter(hgvs = params['pk'])
        serializer = serializers.VariantMetaDataSerializer(response, many=True)
        return  Response(serializer.data)
 
  
  
  
  
# urls.py
router = routers.DefaultRouter()
router.register("VariantMetaDataUsingHGVScDNA", api.VariantMetaDataUsingHGVScDNAViewSet , basename='GetVariantMetaDataUsingHGVScDNA' )

urlpatterns = ( path("api/v1/", include(router.urls)))


# serializers.py
class VariantTranscriptMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant_Transcript

        fields = [
            'pk',
         'meta_data'
        ]

#https://www.youtube.com/watch?v=ws0jwg1J0BU
