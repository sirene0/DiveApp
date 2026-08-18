
from django.core.exceptions import ValidationError

from decompression.models import DecompressionModel

SURFACE_PRESSURE = 1.0  
N2_SURFACE = 0.79
WATER_PRESSURE_PER_METER = 0.1

COMPARTMENTS = [
    {"ID": 1, "half_time": 4.0, "m_value": 3.3},
    {"ID": 2, "half_time": 8.0, "m_value": 2.8},
    {"ID": 3, "half_time": 12.5, "m_value": 2.4},
    {"ID": 4, "half_time": 18.5, "m_value": 2.2},
    {"ID": 5, "half_time": 27.0, "m_value": 2.0},
    {"ID": 6, "half_time": 38.3, "m_value": 1.9},
    {"ID": 7, "half_time": 54.3, "m_value": 1.8},
    {"ID": 8, "half_time": 77.0, "m_value": 1.7},
    {"ID": 9, "half_time": 109.0, "m_value": 1.6},
    {"ID": 10, "half_time": 146.0, "m_value": 1.5},
    {"ID": 11, "half_time": 187.0, "m_value": 1.5},
    {"ID": 12, "half_time": 239.0, "m_value": 1.4},
    {"ID": 13, "half_time": 305.0, "m_value": 1.4},
    {"ID": 14, "half_time": 390.0, "m_value": 1.3},
    {"ID": 15, "half_time": 498.0, "m_value": 1.3},
    {"ID": 16, "half_time": 635.0, "m_value": 1.2},
]



def calculate_inspired_n2(depth,nitrogen_percentage):
    pressure = depth*WATER_PRESSURE_PER_METER + SURFACE_PRESSURE
    gas_fraction = nitrogen_percentage /100
    charge_N2 = pressure * gas_fraction 
    
    return charge_N2

def calculate_compartment_pressure(p_initial, p_inspired, duration, half_time):
    P_tissu_final = p_initial+ (p_inspired - p_initial) *(1-2**(-duration/half_time))
    return P_tissu_final

def calculate_all_compartments (depth,duration,nitrogen_percentage):
    p_inspired = calculate_inspired_n2(depth,nitrogen_percentage)
    compartment_pressures = []
    for c in COMPARTMENTS:
        p_final = calculate_compartment_pressure(
            p_initial = N2_SURFACE,
            p_inspired=p_inspired,
            duration=duration,
            half_time=c['half_time']
        )
        compartment_pressures.append({
            'compartment_id': c['ID'],
            'p_final': round(p_final, 4),
            'm_value': c['m_value'],
            'is_safe': p_final <= c['m_value']
        })
    return compartment_pressures

class decompressionService:
    @staticmethod
    def check_safe_ascente_speed(ascend_speed):
        
            
        safe_ascent_speed = 9
        if ascend_speed > safe_ascent_speed:
            return {
                'status': 'danger',
                'message': f'Ascent speed of {ascend_speed} meters per minute exceeds the safe limit of {safe_ascent_speed} meters per minute.'
            }
        else:
            return {
                'status': 'safe',
                'message': f'Ascent speed of {ascend_speed} meters per minute is within the safe limit.'
            }
        
    @staticmethod
    def calculate_nitrogen_load(depth, duration,nitrogen_percentage):
        compartments = calculate_all_compartments(depth, duration, nitrogen_percentage)

        most_loaded = max(compartments, key=lambda c: c['p_final'])
        all_safe = all(c['is_safe'] for c in compartments)


        return {
            'compartments':   compartments,
            'most_loaded':    most_loaded,
            'all_safe':       all_safe,
            'status': 'safe' if all_safe else 'danger'
        }

    @staticmethod
    def calculate_decompression_Stops(depth ,duration, nitrogen_percentage):
        result = decompressionService.calculate_nitrogen_load(depth, duration, nitrogen_percentage)
        if result['status'] == 'safe':
            return []
        
        stops = []
        current_depth = depth-3
        while current_depth > 0:
            compartments= calculate_all_compartments(current_depth, duration, nitrogen_percentage)
            if all(c['is_safe'] for c in compartments):
                current_depth -= 3
                continue
            most_loaded = max(compartments, key=lambda c: c['p_final'])
            stop_duration =round(   most_loaded['p_final'] / most_loaded['m_value'] * 10, 1)
            stops.append({'depth': current_depth, 'duration_min': stop_duration})
            current_depth -= 3

        return stops

    @staticmethod
    def generate_decompression_plan(dive):
        depth = dive.depth
        duration = dive.duration
        nitrogen_percentage = dive.gas_mix.nitrogen_percentage

        nitrogen_reslt = decompressionService.calculate_nitrogen_load(depth, duration, nitrogen_percentage)
        stops = decompressionService.calculate_decompression_Stops(depth, duration, nitrogen_percentage)
        ascend_speed_check = decompressionService.check_safe_ascente_speed(dive.ascend_Speed)

        DecompressionModel.objects.filter(dive=dive).delete()
        for i,stop in enumerate (stops):
            DecompressionModel.objects.create(
                dive=dive,
                name=f"Palier {i + 1}",
                depth=stop['depth'],
                duration=stop['duration_min'],
                order_number=i + 1,
            )
        return {
            'nitrogen_load': nitrogen_reslt,
            'decompression_stops': stops,
            'ascend_speed_check': ascend_speed_check,
            'requires_decompression': len(stops) > 0
        }
        