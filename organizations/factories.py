
import factory
from factory.django import DjangoModelFactory

from locations.factories import LocationFactory
from organizations.models import Organization


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker(
        "random_element",
        elements=(
            "Instituto Nicaragüense de Estudios Territoriales",
            "Servicio Nacional de Meteorología de Nicaragua",
            "Centro de Investigaciones Hídricas de Nicaragua", 
            "Instituto Nacional de Recursos Naturales",
            "Centro de Monitoreo Ambiental de Nicaragua",
            "Fundación Nicaragüense para el Desarrollo Sostenible",
            "Instituto de Protección y Sanidad Agropecuaria",
            "Centro Nacional de Diagnóstico y Referencia",
            "Instituto de Fomento Municipal de Nicaragua",
            "Empresa Nicaragüense de Acueductos y Alcantarillados",
        )
    )
    
    code = factory.Sequence(lambda n: f"ORG-{n:04d}")
    
    phone = factory.Faker(
        "random_element",
        elements=(
            "+505-2-2234567",
            "+505-2-2445678",
            "+505-8-8234567",
            "+505-8-7345678",
            "+505-5-5234567",
            "+505-7-7456789",
            "+505-2-2334455",
            "+505-2-2567890",
        )
    )
    
    address = factory.Faker(
        "random_element", 
        elements=(
            "Km 12 Carretera Norte, Managua",
            "Centro Comercial Metrocentro, Módulo C-15, Managua",
            "Pista Jean Paul Genie, Casa 234, Managua",
            "Del Hospital Militar 3c al Norte, Managua",
            "Rotonda El Güegüense 200m al Sur, Managua",
            "Barrio Martha Quezada, Calle Principal, Managua",
            "Frente al Parque Central, León",
            "Calle La Calzada, Casa 45, Granada",
            "Del Mercado Central 2c al Este, Estelí",
            "Barrio San José, Contiguo al INSS, Managua",
        )
    )
    
    location = factory.SubFactory(LocationFactory)
