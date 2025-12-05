from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, abort, redirect, url_for, jsonify
from flask_ckeditor import CKEditor
import os
from db import db_session
from db_helpers import get_joined_recipe_from_db, get_active_recipes, get_active_blog_posts, get_single_blog_post_by_slug # Removed - seed_categories, get_all_categories
from werkzeug.exceptions import HTTPException
#Blueprints
from admin.routes import admin_bp


load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = False
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


# categories = get_all_categories()

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(HTTPException)
def error_page(error):
    return render_template('error-page.html', error=error), error.code


@app.route('/merch-store')
def merch():
    return render_template('merch.html')


@app.route('/recipes')
def recipes():
    active_recipes = get_active_recipes()
    data = {
        'type': 'Recipes'
    }
    return render_template('show-recipes-blogs.html', objects=active_recipes, data=data)


@app.route('/recipes/<slug>')
def recipe(slug):
    # recipe = recipe_lookup.get(slug)
    recipe = get_joined_recipe_from_db('slug', slug)
    if not recipe or not recipe.is_active:
        abort(404)
    return render_template('recipe.html', recipe=recipe)


@app.route('/blog')
def blog_posts():
    active_posts = get_active_blog_posts()
    data = {
        'type': 'Blog'
    }
    return render_template('show-recipes-blogs.html', objects=active_posts, data=data)


@app.route('/blog/<slug>')
def show_blog_post(slug):
    post = get_single_blog_post_by_slug(slug)
    if not post or not post.is_active:
        print('====no post====')
        abort(404)
    return render_template('blog-post.html', post=post)


@app.route('/dough-calculator')
def do_calc():
    return render_template('calculator.html')


@app.route('/blog')
def blog():
    active_recipes = get_active_recipes()
    data = {
        'type': 'Blog'
    }
    return render_template('show-recipes-blogs.html', objects=active_recipes, data=data)

# seed_categories()

if __name__ == '__main__':
    app.run(debug=True)