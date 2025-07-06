import os
from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
import serpapi

class FlightsInput(BaseModel):
    departure_airport: Optional[str] = Field(description='Departure airport code (IATA)')
    arrival_airport: Optional[str] = Field(description='Arrival  airport code (IATA)')
    outbound_date: Optional[str] = Field(description='Parameter defines the outbound date. The format is YYYY-MM-DD. e.g. 2025-07-01')
    return_date: Optional[str] = Field(description='Parameter defines the return date. The format is YYYY-MM-DD..g. 2025-07-01')
    adults: Optional[str] = Field(1, description='Parameter defines the number of adults. Default to 1')
    children: Optional[str] = Field(0, description='Parameter defines the number of children. Default to 0.')
    infants_in_seat: Optional[str] = Field(0, description='Parameter defines the number of infants in seat. Default to 0.')
    infants_on_lap: Optional[str] = Field(0, description='Parameter defines the number of infants on lap. Default to 0.')

class FlightsInputSchema(BaseModel):
    params: FlightsInput


@tool(args_schema=FlightsInputSchema)
def flights_finder(params: FlightsInput):
    """
    Find flights using the Google Flights engine.

    Returns:
        dict: Flight search result.
    """
    params = {
        'api_key': os.environ.get("SERPAPI_API_KEY"),
        'engine': 'google_flights',
        'hl': 'en',
        'gl': 'us',
        'departure_id': params.departure_airport,
        'arrival_id': params.arrival_airport,
        'outbound_date': params.outbound_date,
        'return_date': params.return_date,
        'currency': "USD",
        'adults': params.adults,
        'infants_in_seat': params.infants_in_seat,
        'stop': '1',
        'infants_on_lap': params.infants_on_lap,
        'children': params.children
    }

    try:
        search  = serpapi.search(params)
        results = search.data['best_flights']
    except Exception as e:
        results = str(e)
    return results
