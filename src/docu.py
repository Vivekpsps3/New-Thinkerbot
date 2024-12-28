from transformers import pipeline
import tesseract


nlp = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)

output = nlp(
    "https://templates.invoicehome.com/invoice-template-us-neat-750px.png",
    "What is the invoice number?"
)

print(output)