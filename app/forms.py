from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from bs4 import BeautifulSoup
import requests


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('The username ' + username +
                                  ' Is already taken. Please, use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('The email address ' + email +
                                  ' Is already taken. Please, use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    vk_page_url = StringField('Public VK profile URL (avatar export)', validators=[Length(min=0, max=140)])

    def validate_vk_page_url(self, vk_page_url):
        url = vk_page_url.data
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.132'
        }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text)
        if soup.find('img', {'class': 'page_avatar_img'}) is None:
            raise ValidationError('Wrong site or non-existing page. Please, use a different page.')
        avatar_node = soup.find('img', {'class': 'page_avatar_img'}).get('src')
        if avatar_node == '/images/deactivated_hid_200.gif' or avatar_node is None:
            raise ValidationError('The page is private. Please, use a different page.')

    submit = SubmitField('Submit')
