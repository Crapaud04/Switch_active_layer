from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt5.QtCore import (  QSettings, 
                            QTranslator, 
                            qVersion, 
                            QCoreApplication,
                            QVariant)
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QMessageBox,QHBoxLayout,QShortcut
from qgis.core import QgsProject,QgsLayerTreeLayer, QgsVectorLayer
from qgis.utils import iface
from qgis.gui import QgsQueryBuilder
from qgis.PyQt.QtXml import QDomDocument

# initialize Qt resources from file resources.py
from .resources import *

class switchactivelayer:

  def __init__(self, iface):
    # save reference to the QGIS interface
    self.iface = iface
    self.first_start = None

  def initGui(self):
  
    self.first_start = True
    #Add toolbar
    self.toolbar = self.iface.addToolBar("Switch_active_layer")
    # create action that will start plugin configuration
    self.actionDown = QAction( QIcon(":/plugins/switch_active_layer/active_layers_down.png"), "Descendre la couche active", self.iface.mainWindow() )
    iface.registerMainWindowAction(self.actionDown,"PgDown")
    self.actionDown.triggered.connect( self.run_down )
    
    self.actionUp = QAction( QIcon(":/plugins/switch_active_layer/active_layers_up.png"), "Monter la couche active", self.iface.mainWindow() )
    iface.registerMainWindowAction(self.actionUp,"PgUp")
    self.actionUp.triggered.connect( self.run_up )
    

    self.toolbar.addAction( self.actionDown )
    self.toolbar.addAction( self.actionUp )
    self.iface.addPluginToMenu( "&Switch active layer", self.actionDown )
    self.iface.addPluginToMenu( "&Switch active layer", self.actionUp )
    
    

  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removePluginMenu("&Switch active layer", self.actionDown)
    self.iface.removePluginMenu("&Switch active layer", self.actionUp)
    self.iface.unregisterMainWindowAction(self.actionDown)
    self.iface.unregisterMainWindowAction(self.actionUp)
    # remove toolbar on plugin unload
    del self.toolbar
    
    

  def run_down(self):
        #Récupère la liste des couches
            layerList = QgsProject.instance().layerTreeRoot().findLayers()
            max_value = len(layerList) #nombre de couche du projet
            
            vlayer = iface.activeLayer() #récupération couche active
            names_layer = [layer.name()for layer in layerList] #on ne récupère que les nom des couches
            index_layer = names_layer.index(vlayer.name())#position active layer
            if (index_layer+1) < max_value :
             order_down = index_layer + 1  #Ajout de 1 pour passer à la couche d'en desous
             new_layer = names_layer[order_down]#Nom de la couche d'en dessous
             new_layer_active = QgsProject.instance().mapLayersByName(new_layer)[0] # selection de la nouvelle couche 
             iface.setActiveLayer(new_layer_active)#Changement de la couche active
            elif (index_layer+1) == max_value:
             new_layer = names_layer[0]#Nom de la couche d'en dessous
             new_layer_active = QgsProject.instance().mapLayersByName(new_layer)[0] # selection de la nouvelle couche 
             iface.setActiveLayer(new_layer_active)#Changement de la couche active
  def run_up(self):
        #Récupère la liste des couches
            layerList = QgsProject.instance().layerTreeRoot().findLayers()
            max_value = len(layerList) #nombre de couche du projet

            vlayer = iface.activeLayer() #récupération couche active
            names_layer = [layer.name()for layer in layerList] #on ne récupère que les nom des couches
            index_layer = names_layer.index(vlayer.name())#position active layer
            
            order_down = index_layer - 1  #Ajout de 1 pour passer à la couche d'en desous
            new_layer = names_layer[order_down]#Nom de la couche d'en dessous
            new_layer_active = QgsProject.instance().mapLayersByName(new_layer)[0] # selection de la nouvelle couche 
            iface.setActiveLayer(new_layer_active)#Changement de la couche active  