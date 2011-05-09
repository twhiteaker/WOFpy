
from sqlalchemy import (Column, Integer, String, ForeignKey, Float, DateTime,
                        Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import daos.base_models as wof_base

#TODO: Andy, please check
param_to_medium_dict = dict(
    air_pressure=wof_base.SampleMediumTypes.AIR,
    air_temperature=wof_base.SampleMediumTypes.AIR,
    chl_concentration=wof_base.SampleMediumTypes.SURFACE_WATER,
    conductivity=wof_base.SampleMediumTypes.SURFACE_WATER,
    current_speed=wof_base.SampleMediumTypes.SURFACE_WATER,
    depth=wof_base.SampleMediumTypes.SURFACE_WATER,
    eastward_current=wof_base.SampleMediumTypes.SURFACE_WATER,
    northward_current=wof_base.SampleMediumTypes.SURFACE_WATER,
    oxygen_concentration=wof_base.SampleMediumTypes.SURFACE_WATER,
    oxygen_saturation=wof_base.SampleMediumTypes.SURFACE_WATER,
    photosynthetically_available_radiation=wof_base.SampleMediumTypes.SURFACE_WATER, #TODO: Correct?
    relative_humidity=wof_base.SampleMediumTypes.AIR,
    salinity=wof_base.SampleMediumTypes.SURFACE_WATER,
    sea_surface_elevation=wof_base.SampleMediumTypes.SURFACE_WATER,
    signifcant_wave_height=wof_base.SampleMediumTypes.SURFACE_WATER,
    signifcant_wave_to_direction=wof_base.SampleMediumTypes.SURFACE_WATER,
    significant_wave_period=wof_base.SampleMediumTypes.SURFACE_WATER,
    specific_conductance=wof_base.SampleMediumTypes.SURFACE_WATER,
    turbidity=wof_base.SampleMediumTypes.SURFACE_WATER,
    vertical_current=wof_base.SampleMediumTypes.SURFACE_WATER,
    voltage=wof_base.SampleMediumTypes.NOT_RELEVANT,
    water_pressure=wof_base.SampleMediumTypes.SURFACE_WATER,
    water_temperature=wof_base.SampleMediumTypes.SURFACE_WATER,
    wind_from_direction=wof_base.SampleMediumTypes.AIR,
    wind_gust=wof_base.SampleMediumTypes.AIR,
    wind_speed=wof_base.SampleMediumTypes.AIR
)

#TODO: Andy, please check
param_to_gen_category_dict = dict(
    air_pressure=wof_base.GeneralCategoryTypes.CLIMATE,
    air_temperature=wof_base.GeneralCategoryTypes.CLIMATE,
    chl_concentration=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    conductivity=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    current_speed=wof_base.GeneralCategoryTypes.HYDROLOGY,
    depth=wof_base.GeneralCategoryTypes.HYDROLOGY,
    eastward_current=wof_base.GeneralCategoryTypes.HYDROLOGY,
    northward_current=wof_base.GeneralCategoryTypes.HYDROLOGY,
    oxygen_concentration=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    oxygen_saturation=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    photosynthetically_available_radiation=wof_base.GeneralCategoryTypes.UNKNOWN, #TODO: Correct?
    relative_humidity=wof_base.GeneralCategoryTypes.CLIMATE,
    salinity=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    sea_surface_elevation=wof_base.GeneralCategoryTypes.HYDROLOGY,
    signifcant_wave_height=wof_base.GeneralCategoryTypes.HYDROLOGY,
    signifcant_wave_to_direction=wof_base.GeneralCategoryTypes.HYDROLOGY,
    significant_wave_period=wof_base.GeneralCategoryTypes.HYDROLOGY,
    specific_conductance=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    turbidity=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    vertical_current=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    voltage=wof_base.GeneralCategoryTypes.INSTRUMENTATION,
    water_pressure=wof_base.GeneralCategoryTypes.HYDROLOGY,
    water_temperature=wof_base.GeneralCategoryTypes.WATER_QUALITY,
    wind_from_direction=wof_base.GeneralCategoryTypes.CLIMATE,
    wind_gust=wof_base.GeneralCategoryTypes.CLIMATE,
    wind_speed=wof_base.GeneralCategoryTypes.CLIMATE,
)


Base = declarative_base()


def clear_model(engine):
    Base.metadata.drop_all(engine)

def create_model(engine):
    Base.metadata.create_all(engine)

def init_model(db_session):
    Base.query = db_session.query_property()

class Site(Base, wof_base.BaseSite):
    __tablename__ = 'Sites'
    
    def __init__(self, code, name, latitude, longitude):
        self.SiteCode = code
        self.SiteName = name
        self.Latitude = latitude
        self.Longitude = longitude
    
    SiteID = Column(Integer, primary_key=True)
    SiteCode = Column(String)
    SiteName = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    
class Units(Base, wof_base.BaseUnits):
    __tablename__ = 'Units'
    
    def __init__(self, name, abbreviation):
        self.UnitsName = name
        self.UnitsAbbreviation = abbreviation
    
    UnitsID = Column(Integer, primary_key=True)
    UnitsName = Column(String)
    #UnitsType = None
    UnitsAbbreviation = Column(String)

   
class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'Variables'
    
    def __init__(self, code, name):
        self.VariableCode = code
        self.VariableName = name
        self.NoDataValue = -9999
        
        if self.VariableCode in param_to_medium_dict:
            self.SampleMedium = param_to_medium_dict[self.VariableCode]
        else:
            self.SampleMedium = wof_base.SampleMediumTypes.UNKNOWN
            
        if self.VariableCode in param_to_gen_category_dict:
            self.GeneralCategory = param_to_gen_category_dict[
                self.VariableCode]
        else:
            self.GeneralCategory = wof_base.GeneralCategoryTypes.UNKNOWN
    
    VariableID = Column(Integer, primary_key=True)
    VariableCode = Column(String)
    VariableName = Column(String)
    VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #Speciation = None
    SampleMedium = Column(String)
    #ValueType = None
    #IsRegular = None
    #DataType = None
    GeneralCategory = Column(String)
    NoDataValue = Column(Integer)
    
    VariableUnits = relationship("Units",
                        primaryjoin='Variable.VariableUnitsID==Units.UnitsID') 
    #TimeUnits = None

'''
class SeriesCatalog(Base, wof_base.BaseSeriesCatalog):
    
    SeriesID = Column(Integer, primary_key=True)
    SiteID = Column(Integer, ForeignKey('Site.SiteID'))
    SiteCode = Column(String)
    SiteName = Column(String)
    VariableID = Column(Intger, ForeignKey('Variable.VariableID'))
    VariableCode = Column(String)
    VariableName = Column(String)
    #Speciation = None
    VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID')) 
    VariableUnitsName = Column(String)
    SampleMedium = Column(String)
    #ValueType = None
    #TimeSupport = None
    #TimeUnitsID = None
    #TimeUnitsName = None
    #DataType = None
    GeneralCategory = Column(String)
    #MethodID = None
    #MethodDescription = None
    #SourceID = None #TODO
    #Organization = None
    #SourceDescription = None
    #Citation = None
    #QualityControlLevelID = None
    #QualityControlLevelCode = None
    #BeginDateTime = None
    #EndDateTime = None
    BeginDateTimeUTC = Column(DateTime)
    EndDateTimeUTC = Column(DateTime)
    ValueCount = Column(Intger)
    
    Site = relationship("Site",
                    primaryjoin="Site.SiteID==SeriesCatalog.SiteID")
    Variable = relationship("Variable",
                    primaryjoin="Variable.VariableID==SeriesCatalog.SiteID")
    
    #Method = None
'''