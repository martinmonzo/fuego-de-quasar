from quasar_fire_app.domain.satellite import get_coordinates_by_satellite_name
from quasar_fire_app.utils.math import (
    is_close,
    ROUND_SIGNIFICANT_DECIMALS,
)


def get_transmitter_location(distances):
    """
    Retrieve the location (X,Y) of a transmitter, given its 
    distance to each satellite, if it's posible to be determined.

    TO CONSIDER:
        The problem requires a trilateration formula in order to be solved. The issue is that 
        the trilateration formula returns a tuple (X,Y) that could be right or not (in case 
        that the problem doesn't have a solution, the value returned by this formula will be wrong). 
        
        So, to determine whether the solution of the formula is right or not, we need to check if 
        this value satisfies the 3 equations, that is, that the retrieved point is at the specified 
        distance from each satellite.

        But, as we know, when we operate with float numbers, there's a data error introduced. E.g.:
        > number = 1.1
        > print(number**2) -> 1.2100000000000002

        The expected value was 1.21, but we got a slightly different number.

        Because of this reason, I implemented a method called is_close, to determine whether the 
        retrieved value and the expected one are "almost" equal. What does "almost" mean? 
        It means that both numbers have by a very little difference, which is determined by an 
        arbitrary error constant that I defined (APPROXIMATION_CONSTANT = 1e-3)

    Args:
        - distances (list[float]): distance from the transmitter to each satellite.
    
    Returns:
        tuple(float, float): (X,Y) coordinates of the transmitter.
    """
    # We assume that the first distance retrieved is the distance from the transmitter to Kenobi
    x1,y1 = get_coordinates_by_satellite_name('kenobi')
    # We assume that the second distance retrieved is the distance from the transmitter to Skywalker
    x2,y2 = get_coordinates_by_satellite_name('skywalker')
    # We assume that the third distance retrieved is the distance from the transmitter to Sato
    x3,y3 = get_coordinates_by_satellite_name('sato')
    
    r1 = distances[0]
    r2 = distances[1]
    r3 = distances[2]

    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2 
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    # Check that the retrieved value (x,y) is enough approximated 
    # to each distance formula -> (x-xi)**2+(y-yi)**2 == ri**2
    if not (
        is_close((x-x1)**2+(y-y1)**2, r1**2)
        and is_close((x-x2)**2+(y-y2)**2, r2**2)
        and is_close((x-x3)**2+(y-y3)**2, r3**2)
    ):
        raise Exception('The retrieved value is not at the specified distances from the satellites.')
    
    return round(x, ROUND_SIGNIFICANT_DECIMALS), round(y, ROUND_SIGNIFICANT_DECIMALS)
