# import requests
# import json
# import openai
# import pdfplumber

# class PDFParsing:

#     def prepare_request(self, pdf_file):
#         self.data = {
#             "applicant_name": "",
#             "applicant_email": "",
#             "applicant_phone": "",
#             "applicant_city": "",
#             "applicant_state": "",
#             "applicant_country": "",
#             "academicCredentials": [{
#                 "degree": "",
#                 "major": "",
#                 "university": "",
#                 "college_location": "",
#                 "year": ""
#             }],
#             "projects": [{
#                 "name": "",
#                 "languages": "",
#                 "database": "",
#                 "softwarePackages": ""
#             }],
#             "Skills": {
#                 "languages": "",
#                 "database": "",
#                 "softwares": "",
#                 "Technologies": ""
#             },
#             "personalInformation": {
#                 "fatherName": "",
#                 "motherName": "",
#                 "dateOfBirth": "",
#                 "gender": "",
#                 "languagesKnown": "",
#                 "maritalStatus": "",
#                 "nationality": ""
#             }
#         }
        
#         request_data = {
#             "inputs": {
#                 "pdf_content": pdf_file,
#                 "data": self.data
#             }
#         }
#         return request_data

#     def send_request(self, api_key, pdf_file):
#         with pdfplumber.open(pdf_file) as pdf:
#             pdf_text = ""
#             for page in pdf.pages:
#                 pdf_text += page.extract_text() + "\n\n"

#         openai.api_key = api_key
#         request_data = self.prepare_request(pdf_text)
#         prompt = json.dumps(request_data)
#         prompt_chunks = [prompt[i:i+4096] for i in range(0, len(prompt), 4096)]
#         response_text = ""

#         for chunk in prompt_chunks:
#             response = openai.Completion.create(
#                 engine="text-davinci-003",
#                 prompt=chunk,
#                 max_tokens=100
#             )
#             response_text += response.choices[0].text

#         return response_text
