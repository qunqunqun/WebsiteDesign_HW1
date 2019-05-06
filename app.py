import uuid

from flask import Flask, render_template, flash, redirect, url_for, session, send_from_directory
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,ValidationError
from flask_wtf.file import FileRequired ,FileField,FileAllowed
from flask_bootstrap import Bootstrap   #导入
from wtforms.validators import Email
import os
import mySql

app = Flask(__name__)
app.secret_key = os.urandom(12)
CurMysql = mySql.Mysql()
bootstrap = Bootstrap(app) #进行绑定操作
CurUsername = str() #是一个str类型，表示当前的名字

@app.route('/index')
def index():
    return render_template("index.html")


class LoginForm(FlaskForm):
    username = StringField('用户名', render_kw={'placeholder': 'you name'}, validators=[DataRequired(message=u"请输入用户名")])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    submit = SubmitField('提交')

class ToRegisterForm(FlaskForm): #选是否是注册
    toRegister = SubmitField('注册')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    email = TextAreaField('Email', validators=[DataRequired(), Email(), Length(1,254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,128)])
    submit2 = SubmitField('Register')

@app.route('/',methods=['GET','POST'])
def ini():
    form = LoginForm()
    reForm = ToRegisterForm()
    if reForm.validate():
        if reForm.toRegister.data:
            return redirect(url_for("multi_form"))
    if form.validate_on_submit():
        if form.submit.data:  # 登录按钮被单击
                #TODO链接数据库进行验证
                if CurMysql.test(form.username.data,form.password.data) == True:
                    print("yes")
                    global CurUsername
                    CurUsername = form.username.data
                    return redirect(url_for("showCus"))
                else:
                    flash('无此用户，请重新登录或者注册')
                    print("No")
                    return render_template('login.html', loginForm=form, toReform=reForm)
                #返回发布页面
    return render_template('login.html',loginForm=form,toReform = reForm)

@app.route('/login',methods=['GET','POST'])  #一般默认提交方式是post，不写get的话不用get方式
def login():
    form = LoginForm()
    reForm = ToRegisterForm()
    if reForm.validate():
        if reForm.toRegister.data:
            return redirect(url_for("multi_form"))
    if form.validate_on_submit():
        if form.submit.data:  # 登录按钮被单击
            # TODO链接数据库进行验证
            if CurMysql.test(form.username.data, form.password.data) == True:
                print("yes")
                global CurUsername
                CurUsername = form.username.data
                return redirect(url_for("showCus"))
            else:
                flash('无此用户，请重新登录或者注册')
                print("No")
                return render_template('login.html', loginForm=form, toReform=reForm)
            # 返回发布页面
    return render_template('login.html',loginForm=form, toReform=reForm)

@app.route('/register', methods=['GET', 'POST'])
def multi_form():
    register_form = RegisterForm()
    #validate()逐个对字段调用字段实例化时定义的验证器，返回表示验证结果的布尔值
    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        if CurMysql.insert(register_form.username.data,register_form.password.data,register_form.email.data) == False:
            flash('已有此用户，请重新注册')
        else:
            global CurUsername
            CurUsername = register_form.username.data
            return redirect(url_for("showCus"))
    return render_template("register.html",register_form = register_form)


#FileUpload
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


class Opeartor(FlaskForm):
    Insert = SubmitField()
    Delete = SubmitField()

@app.route('/show', methods=['GET', 'POST'])
def showCus():
    form = Opeartor()
    #展示自己的物品
    flash("您要卖的物品如下，您可添加或者删除")
    global CurUsername
    print(CurUsername,"的物品展示")
    thing_list = CurMysql.FindMyThing(CurUsername)
    if form.Insert.data: #转到添加页面
        print("click insert")
        return redirect(url_for('upload'))
    elif form.Delete.data: #转到删除页面
        return redirect(url_for('deleteThing'))

    return render_template('showThing.html',thing_list = thing_list,form = form)

class UploadForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 20)])
    des = TextAreaField('description', validators=[DataRequired(), Length(30, 100)])
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg'])])
    submit = SubmitField()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        T_name = form.name.data
        T_des = form.des.data
        C_Name = CurUsername #当前人的信息
        f = form.photo.data #当前图片的信息
        filename = C_Name + "_"+ T_name.__str__() + ".jpg"  #名字为qun + _+ 物品名
        if CurMysql.CheckInsert(C_Name,T_name,T_des,filename) == False: #不能加入
            return render_template('upload.html', form=form)
        #否则保存图片
        upload_foler = app.root_path + '//static//images'
        f.save(upload_foler + '//'+filename)
        flash("Upload Success")
        return redirect(url_for('showCus'))
    else:
        return render_template('upload.html',form = form)


class DeleteForm(FlaskForm):
    T_Name = StringField('物品名称', validators=[DataRequired(), Length(1,40)])
    mysubmit = SubmitField() #提交删除按钮
    cancel = SubmitField()  #返回

@app.route('/deleteThing',methods=['GET', 'POST'])
def deleteThing():
    form = DeleteForm()
    if form.validate_on_submit():
        if form.mysubmit.data: #提交删除按钮
            if CurMysql.deFromDB(CurUsername,form.T_Name.data) == False:
                flash("输入商品错误，请重新输入")
                return render_template("deleteThing.html", form=form)
            else:
                flash("删除成功")
                return redirect(url_for('showCus'))
        elif form.cancel.data: #提交返回按钮
            return redirect(url_for('showCus'))
    return render_template("deleteThing.html",form = form)

if __name__ =='__main__':
    app.run()
