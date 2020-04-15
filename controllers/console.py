from gluon.packages.dal.pydal.validators import IS_DATE
from gluon.serializers import loads_json
from gluon.tools import fetch
from plugin_daxs_utils import console

@console
def update_data():
    data = loads_json(fetch(configuration.get('app.cases_data_source_url')))
    casos = data['casos']
    dias = casos['dias']

    # db.casos.fecha.requires = IS_DATE(format=('%Y/%m/%d'))
    # db.casos.arribo_a_cuba_foco.requires = IS_DATE(format=('%Y/%m/%d'))
    # db.casos.consulta_medico.requires = IS_DATE(format=('%Y/%m/%d'))

    for dia in dias.keys():
        fecha = dias[dia]['fecha']
        if 'diagnosticados' not in dias[dia]:
            continue
        diagnosticados_dia = dias[dia]['diagnosticados']
        for diagnosticado in diagnosticados_dia:
            diagnosticado['arribo_a_cuba_foco'] = diagnosticado['arribo_a_cuba_foco'].replace('/', '-') if diagnosticado['arribo_a_cuba_foco'] else diagnosticado['arribo_a_cuba_foco']
            diagnosticado['consulta_medico'] = diagnosticado['consulta_medico'].replace('/', '-') if diagnosticado['consulta_medico'] else diagnosticado['consulta_medico']

            diagnosticado['codigo'] = diagnosticado['id']
            del diagnosticado['id']
            diagnosticado['fecha'] = fecha.replace('/', '-') if fecha else fecha
            diagnosticado['dia'] = dia
            db.casos.update_or_insert(db.casos.codigo == diagnosticado['codigo'], **diagnosticado)
            # db.casos.insert(**diagnosticado)
    db.commit()
    return True


    # print('akakak', data['casos'])