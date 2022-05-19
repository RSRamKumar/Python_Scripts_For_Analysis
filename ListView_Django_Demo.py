from datetime import date
from django.db.models import Q

class VariantsWithOldReviewDate(generic.ListView):
    model = Evaluation

    def get_queryset(self):
        
        # query the entire model 
        print( Evaluation.objects.all().count())
        
        # to find unique reviewed_date
        print(Evaluation.objects.all().values('reviewed_date').distinct().order_by('reviewed_date'))

        # to count our results
        # print(Evaluation.objects.filter(reviewer=None).count())

        # filter based on condition 'reviewed_date: None ' present and sorting it for our convenience


        #print(Evaluation.objects.filter(reviewed_date =None).order_by('variant').count())
        #print(Evaluation.objects.filter(reviewed_date =None).order_by('variant'))

        print('without querying')
        print(Evaluation.objects.filter(reviewed_date__year__lte = date.today().year-2).count())
        print(Evaluation.objects.filter(reviewed_date = None ).count())

        print('after querying')
        print(Evaluation.objects.filter(Q(reviewed_date__year__lte=date.today().year - 2) |
                                        Q(reviewed_date=None)).count())
        return Evaluation.objects.filter(reviewed_date__year__lte = date.today().year-2).order_by('reviewed_date')







    
