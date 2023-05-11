from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
items = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           product_name = list(popular_df['Grocery-Title'].values),
                           author=list(popular_df['Book-Price'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_inputt = request.form.get('user_input').lower()
    ppp = np.where(pt.index == user_inputt)[0]
    print("length",len(ppp))
    if len(ppp)>0:
        user_input = request.form.get('user_input').lower()
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[0:11]

        data = []
        for i in similar_items:
            item = []
            temp_df = items[items['Grocery-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Grocery-Title')['Grocery-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Grocery-Title')['Book-Price'].values))
            item.extend(list(temp_df.drop_duplicates('Grocery-Title')['Image-URL-M'].values))
            


            data.append(item)

        print("jkjk",data)

        return render_template('recommend.html',data=data)
    else:
        return render_template('recommend.html')

if __name__ == '__main__':
    app.run(debug=True)