
from repository.database import DataBase
from jinja2 import FileSystemLoader, Environment


class Generator:
    def __init__(self, tables:list, env="development"):
        self.__tables__ = tables
        self.__env__ = env


    def generator_model(self):
        for t in self.__tables__:
            name = lambda x: "".join([i.title() for i in str(x).split("_")])+"Model"
            namefile = lambda x: "".join([i for i in str(x).split("_")])+"model"
            columns_data = DataBase(t, self.__env__).columns
            indexes = DataBase(t, self.__env__).index
            getindexes = lambda: (", ".join(indexes))
            getindexeswhere = lambda comp="": " AND ".join([f"{i} = '{{{comp}{i}}}'" for i in indexes])
            getindexesif = lambda: " and ".join([f"self.{i}" for i in indexes])
            columns = ([f'''self.{c} = None''' for c in columns_data])
            
            fromdict = [f'''obj.{c} = dct.get('{c}')''' for c in columns_data]
            todict = [f'''"{c}": self.{c},''' for c in columns_data]
            
            template =  Environment(loader= FileSystemLoader(searchpath="generators")).get_template("model_generator.gn")
            model = template.render(columns=columns, name=name, t=t, fromdict=fromdict, todict=todict, getindexeswhere=getindexeswhere, getindexes=getindexes, getindexesif=getindexesif)
            print(model)
            
            with open("models/"+namefile(t)+".py", "w") as f: f.write(str(model))
        return self

    def generator_handler(self):
        name = lambda x: "".join([i.title() for i in str(x).split("_")])+"Model"
        namefile = lambda x: "handler"+"".join([i for i in str(x).split("_")]).title()
        namefilemodel = lambda x: "".join([i for i in str(x).split("_")])+"model"
        handlername = lambda x: "Handler"+"".join([i.title() for i in str(x).split("_")])
        
        for t in self.__tables__:
            template =  Environment(loader= FileSystemLoader(searchpath="generators")).get_template("handler_generator.gn")
            model = template.render(t=t, namefile=namefile, name=name, namefilemodel=namefilemodel, handlername=handlername)
            print(model)
            
            with open("handler/"+namefile(t)+".py", "w") as f: f.write(str(model))
            
        return self
            
    
    def generator_blueprint(self):
        
        for t in self.__tables__:
            handlername = "Handler"+"".join([i.title() for i in str(t).split("_")])
            handlerfile = "handler"+"".join([i.title() for i in str(t).split("_")])
            route_name = "_".join([i.lower() for i in str(t).split("_")])
            route_endpoint = "/".join([i.lower() for i in str(t).split("_")])
            template =  Environment(loader= FileSystemLoader(searchpath="generators")).get_template("route_generator.gn")
            model = template.render(t=t, route_name=route_name, route_endpoint=route_endpoint, handlername=handlername, handlerfile=handlerfile)
            print(model)
           
            with open("routes/route_"+route_name+".py", "w") as f: f.write(str(model))
            
            initdata = ""
            
            with open('routes/__init__.py', 'r') as file:
                initdata = file.read()
                if "route_"+route_name not in  initdata:
                    initdata += f"from .route_{route_name} import route_{route_name}\n"
                print(initdata)
            
            with open('routes/__init__.py', 'w') as file: file.write(initdata)
            
            serverdata = ""
            with open('server.py', 'r') as file:
                serverdata = file.read()
                if "route_"+route_name not in  serverdata:
                    serverdata += f"app.register_blueprint(route_{route_name})\n"
                print(serverdata)
            
            with open('server.py', 'w') as file: file.write(serverdata)
            
            
            
        return self
    

if __name__ == '__main__':
    tables = ['client', 'product']
    Generator(tables=tables).generator_model().generator_handler().generator_blueprint()
    # generator_handler(tables)
    