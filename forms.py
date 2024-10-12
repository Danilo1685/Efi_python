from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import Length, DataRequired



class MarcaForm(FlaskForm):
    nombre= StringField(
        'Nombre',
        validators=[Length(min=3, max=40), DataRequired()],
        render_kw={"class":"form-control", "placeholder":"Nombre"}
    )
    submit= SubmitField(
        'Guardar',
        render_kw={"class":"form-control btn btn-success"}
        )


class TipoForm(FlaskForm):
    nombre= StringField(
        'Nombre',
        validators=[Length(min=3, max=40), DataRequired()],
        render_kw={"class":"form-control", "placeholder":"Nombre"}
    )
    submit= SubmitField(
        'Agregar',
        render_kw={"class":"form-control btn btn-success"}
        )


class TelefonoForm(FlaskForm):
    modelo = StringField('Modelo', validators=[DataRequired()])
    anio_fabricacion = IntegerField('Año de Fabricación', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    accesorio = SelectField('Accesorio', coerce=int)
    marca = SelectField('Marca', coerce=int)
    tipo = SelectField('Tipo', coerce=int)
    submit = SubmitField('Agregar')


class AccesorioForm(FlaskForm):
    nombre= StringField(
        'Nombre',
        validators=[Length(min=3, max=40), DataRequired()],
        render_kw={"class":"form-control", "placeholder":"Nombre"}
    )
    submit= SubmitField(
        'Agregar',
        render_kw={"class":"form-control btn btn-success"}
        )


