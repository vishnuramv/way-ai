from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from transformers import pipeline
from flask_cors import CORS
gen_model = "./models/way-model/"
summarize_model = "./models/way-sum-model/"

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

generator = pipeline(task='text-generation', model=gen_model)
summarizer = pipeline("summarization", model=summarize_model, tokenizer=summarize_model, framework="tf")
class GenerateBlog(Resource):
    def post(self):
        data = request.get_json()  
        text = data['text']
        response_ouput = []
        generator_output = generator(text,max_length=500, num_return_sequences=5)
        for i in range(len(generator_output)):
            temp = {}
            temp['text'] = generator_output[i]['generated_text']
            response_ouput.append(temp)
        print(response_ouput)
        res = {
            'status': 'success',
            'data': response_ouput,
            'code': 200
        }
        return jsonify(res)

class Summarize(Resource):
    def post(self):
        data = request.get_json() 
        text = data['text']
        response_ouput = summarizer(text, min_length=100, do_sample=False)[0]['summary_text']
        res = {
            'status': 'success',
            'data': response_ouput,
            'code': 200
        }
        return jsonify(res)

api.add_resource(GenerateBlog, '/')
api.add_resource(Summarize, '/summarize')

if __name__ == '__main__':
    app.run(debug=True)