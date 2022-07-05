from dao_visualization import DAO_visualization


class API_visualization():
    def __init__(self):
        self.data = {}
        self.dao = DAO_visualization()
        self.__extractData()

    def getData(self):
        return self.data

    def __extractData(self):
        self.data = self.dao.getJSONs()