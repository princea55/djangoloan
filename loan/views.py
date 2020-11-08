from django.shortcuts import render
from .apps import LoanConfig
from django.http import JsonResponse
from rest_framework.views import APIView
import pandas as pd
class call_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            return render(request, 'index.html')

    def post(self, request):
        if request.method == 'POST':
            # get sound from request
            Gender = request.POST.get('Gender')
            Married = request.POST.get('Married')
            Dependents = request.POST.get('Dependents')
            Education = request.POST.get('Education')
            Self_Employed = request.POST.get('Self_Employed')
            Applicant_Income = request.POST.get('Applicant_Income')
            Coapplicant_Income = request.POST.get('Coapplicant_Income')
            Loan_Amount = request.POST.get('Loan_Amount')
            Loan_Amount_Term = request.POST.get('Loan_Amount_Term')
            Credit_History = request.POST.get('Credit_History')
            Property_Area = request.POST.get('Property_Area')
            # np.array([income,age,rooms,bedrooms,population])
            
            
            
            price = {'Gender': [int(Gender)],
                'Married': [int(Married)],
                'Dependents': [int(Dependents)],
                'Education': [int(Education)],
                'Self_Employed': [int(Self_Employed)],        
                'Applicant_Income': [int(Applicant_Income)],        
                'Coapplicant_Income': [int(Coapplicant_Income)],        
                'Loan_Amount': [int(Loan_Amount)],        
                'Loan_Amount_Term': [int(Loan_Amount_Term)],        
                'Credit_History': [int(Credit_History)],        
                'Property_Area': [int(Property_Area)],    
                        
                }
            df = pd.DataFrame(price,columns=['Gender','Married','Dependents','Education','Self_Employed','Applicant_Income','Coapplicant_Income','Loan_Amount','Loan_Amount_Term','Credit_History','Property_Area']) 
            # vectorize sound
            # vector = PricepredictorConfig.vectorizer.transform([income,age,rooms,bedrooms,population])
            new_row = {'Gender':1, 'Married':1, 'Dependents':2, 'Education':1, 'Self_Employed':0, 'Applicant_Income':10000, 'Coapplicant_Income':2000, 'Loan_Amount':208, 'Loan_Amount_Term':200, 'Credit_History':1, 'Property_Area':2}

            df = df.append(new_row, ignore_index=True)

            from sklearn.decomposition import PCA
            pca = PCA(n_components = 2)
            testab = pca.fit_transform(df)
            explained_variance = pca.explained_variance_ratio_
            

            # predict based on vector
            prediction = LoanConfig.classifier.predict(testab)[0]
            print(prediction)
            
            if(int(prediction) == 1):
                eligible = "1234"
            else:
                eligible = "0"    
                
           
            
            # build response
            response = {
                'eligibility': eligible,
                'status':int(prediction)
                }
            
            # return response
            # return JsonResponse(response)
            return render(request, 'index.html',response)