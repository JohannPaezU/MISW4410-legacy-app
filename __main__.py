import sys
from src.vista.InterfazRecetario import App_Recetario
from src.logica.LogicaMock import LogicaMock
from src.logica.Logica import Logica
from src.modelo.declarative_base import session, Base, engine

if __name__ == '__main__':
    # Punto inicial de la aplicación
    Base.metadata.create_all(engine)
    session.close()

    logicaMock = LogicaMock()
    logica = Logica()

    #app = App_Recetario(sys.argv, logicaMock)
    app = App_Recetario(sys.argv, logica)
    sys.exit(app.exec_())