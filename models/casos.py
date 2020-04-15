from gluon.packages.dal.pydal.validators import IS_IN_SET

db.define_table('casos',
                Field('codigo', 'string', label=T('code')),
                Field('dia', 'integer', label=T('day')),
                Field('fecha', 'date', label=T('date')),
                Field('pais', 'string', label=T('country')),
                Field('edad', 'integer', label=T('age')),
                Field('sexo', 'string', reqires=IS_IN_SET(['hombre', 'mujer']), label=T('sex')),
                Field('arribo_a_cuba_foco', 'date', label=T('Arrive to Cuba')),
                Field('consulta_medico', 'date', label=T('Consultation')),
                Field('municipio_detección', 'string', label=T('Municipality')),
                Field('provincia_detección', 'string', label=T('Province')),
                Field('dpacode_municipio_deteccion', 'string', label=T('Municipality code')),
                Field('dpacode_provincia_deteccion', 'string', label=T('Province code')),
                Field('contagio', 'string', reqires=IS_IN_SET(['importado', 'introducido']), label=T('Contagion')),
                Field('contacto_focal', 'integer', label=T('Focal Contact')),
                Field('centro_aislamiento', 'string', label=T('Isolation center')),
                Field('centro_diagnostico', 'string', label=T('Diagnostic center')),
                Field('posible_procedencia_contagio', 'list:string', label=T('Possible origin of contagion')),
                Field('info', 'text', label=T('Info')),
                Field('provincias_visitadas', 'list:string', label=T('Visited provinces')),
                Field('dpacode_provincias_visitadas', 'list:string', label=T('Code of visited provinces')),
                )

# db.casos.fecha.requires = IS_DATE(format=('%Y/%m/%d'))
# db.casos.arribo_a_cuba_foco.requires = IS_DATE(format=('%Y/%m/%d'))
# db.casos.consulta_medico.requires = IS_DATE(format=('%Y/%m/%d'))
