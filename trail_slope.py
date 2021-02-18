from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class TrailSlope(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('DEM', 'DEM', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('trailfile', 'trail_file', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Trail_slope_final', 'trail_slope_final', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Split lines by maximum length
        alg_params = {
            'INPUT': parameters['trailfile'],
            'LENGTH': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SplitLinesByMaximumLength'] = processing.run('native:splitlinesbylength', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Drape (set Z value from raster)
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['SplitLinesByMaximumLength']['OUTPUT'],
            'NODATA': 0,
            'RASTER': parameters['DEM'],
            'SCALE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DrapeSetZValueFromRaster'] = processing.run('native:setzfromraster', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'slope',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'abs(z(start_point($geometry)) - z(end_point($geometry)))/$length*100',
            'INPUT': outputs['DrapeSetZValueFromRaster']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['Trail_slope_final']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Trail_slope_final'] = outputs['FieldCalculator']['OUTPUT']
        return results

    def name(self):
        return 'Trail Slope'

    def displayName(self):
        return 'Trail Slope'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return TrailSlope()
