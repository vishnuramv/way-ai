from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

class GenerateBlog(Resource):
    def post(self):
        data = request.get_json()  
        text = data['text']
        response_ouput = []
        generator_output = openai.Completion.create(
            model="text-curie-001",
            prompt=text,
            max_tokens=256,
            n=2,
            temperature=0.8
        ).choices
        print(generator_output) 
        for i in range(len(generator_output)):
            temp = {}
            temp['text'] = generator_output[i]['text']
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
        response_ouput = openai.Completion.create(
            model="text-curie-001",
            prompt="Summarize the given text into 50 words: " + text,
            max_tokens=256,
            temperature=1.5,
            presence_penalty=1,
            frequency_penalty=1,
            top_p=1,
            best_of=5
        ).choices[0].text
        print(response_ouput)
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