from observer import controller_cython as controller
cont = controller.Controller('/home/ubuntu/settings_triangle.conf','live')
cont.retrieve_data(4, completed = False, upsert = True)
cont.data2sheet(complete = False)
allowed_ins = [ins.name for ins in cont.allowed_ins]
returns = [cont.open_limit(ins, close_only = True, complete = False) for ins in allowed_ins]
cont_demo = controller.Controller('/home/ubuntu/settings_triangle.conf','demo')
returns = [cont_demo.open_limit(ins, close_only = True, complete = False) for ins in allowed_ins]
