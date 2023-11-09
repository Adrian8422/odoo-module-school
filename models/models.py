from odoo import models,fields,api

class Alumno (models.Model):
    _name='school.alumno'
    _description = 'school.alumno'

    name = fields.Char()
    apellido = fields.Char(string='Apellido', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    nro_legajo = fields.Char(string='Nro de Legajo')
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    direccion = fields.Char(string='Dirección')
    pais = fields.Char(string='País')

    programas_inscritos = fields.Many2many('school.programa', 'inscripcion_alumno_rel', 'alumno_id', 'inscripcion_id',
                                        string='Programas Inscritos',invisible=True)



class Programa (models.Model):
    _name='school.programa'
    _description='school.programa'

    name= fields.Char(string='Nombre', required=True)
    descripcion= fields.Char(string='Descripcion', required=False)
    inscripcion_ids = fields.One2many('school.inscripcion', 'programa_id', string='Inscripciones')
    alumnos_inscritos = fields.Many2many('school.alumno', string='Alumnos Inscritos', compute='compute_alumnos_inscritos',invisible=True)



    def compute_alumnos_inscritos(self):
        for programa in self:
            programa.alumnos_inscritos = programa.inscripcion_ids.mapped('alumno_id')

    def get_alumnos_inscritos(self):
        self.compute_alumnos_inscritos()
        action = {
            'name': 'Data from Method',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'view_type': 'tree',
            'res_model': 'school.inscripcion',
            'target': 'current',
            'domain': [('id', 'in', self.alumnos_inscritos.ids)],
            'view_id': self.env.ref('school.programa_alumnos_inscritos_list').id,
        }
        return action    

    
    
    # def obtener_alumnos_inscriptos(self):
    #     alumnos=[]
    #     for inscripcion in self.inscripciones_ids:
    #         alumno = {
    #             'nombre':inscripcion.alumno_id.nombre,
    #             'apellido':inscripcion.alumno_id.apellido,
    #             'legajo':inscripcion.alumno_id.legajo,
    #             'fecha_nacimiento':inscripcion.alumno_id.fecha_nacimiento,
    #             'email':inscripcion.alumno_id.email,
    #             'telefono':inscripcion.alumno_id.telefono,
    #             'pais':{
    #                 'id':inscripcion.alumno_id.pais.id,
    #                 'nombre':inscripcion.alumno_id.pais.nombre
    #             }

    #         }
    #         alumnos.append(alumno)
    #     return alumnos  




class Inscripcion(models.Model):
    _name = 'school.inscripcion'
    _description = 'Inscripción a Programa'

    alumno_id = fields.Many2one('school.alumno', string='Alumno',)
    programa_id = fields.Many2one('school.programa', string='Programa',)
    fecha_inscripcion = fields.Date(string='Fecha de Inscripción', default=fields.Date.today)


    alumno_nombre = fields.Char(related='alumno_id.name', string='Nombre', store=True)
    alumno_apellido = fields.Char(related='alumno_id.apellido', string='Apellido', store=True)
    alumno_legajo = fields.Char(related='alumno_id.nro_legajo', string='Nro de Legajo', store=True)
    alumno_fecha_nacimiento = fields.Date(related='alumno_id.fecha_nacimiento', string='Fecha de Nacimiento', store=True)
    alumno_email = fields.Char(related='alumno_id.email', string='Email', store=True)
    alumno_telefono = fields.Char(related='alumno_id.telefono', string='Teléfono', store=True)

    alumnos_inscritos = fields.Many2many('school.alumno', 'inscripcion_alumno_rel', 'inscripcion_id', 'alumno_id',
                                        related='programa_id.alumnos_inscritos', string='Alumnos Inscritos', invisible=True)

    _sql_constraints = [
        ('alumno_programa_unique', 'unique(alumno_id, programa_id)', 'El alumno ya está inscrito en este programa.'),
    ]