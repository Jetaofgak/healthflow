package com.example.healthflow.service;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import com.example.healthflow.model.FhirBundleEntity;
import com.example.healthflow.repository.FhirBundleRepository;
import org.hl7.fhir.r4.model.Bundle;
import org.springframework.stereotype.Service;
import org.hl7.fhir.r4.model.Observation;
import ca.uhn.fhir.model.api.Include;

@Service
public class FhirSyncService {

    private final FhirBundleRepository repository;
    private final IGenericClient fhirClient;
    private final FhirContext ctx;
    
    public FhirSyncService(FhirBundleRepository repository, 
                           @Value("${fhir.server.url:https://hapi.fhir.org/baseR4}") String fhirServerUrl) {
        this.repository = repository;
        this.ctx = FhirContext.forR4();
        
        // On utilise la variable injectée
        this.fhirClient = ctx.newRestfulGenericClient(fhirServerUrl);
        System.out.println("Connecting to FHIR Server: " + fhirServerUrl);
    }

    public String syncPatientData(String patientId) {
        // 1. Appel au serveur FHIR distant
        Bundle bundle = fhirClient
                .search()
                .forResource("Observation")
                // 1. Filtrer les observations de CE patient
                .where(Observation.PATIENT.hasId(patientId))
                // 2. Inclure le patient lui-même dans la réponse
                .include(new Include("Observation:patient"))
                // 3. (Optionnel) Inclure tout recursivement si besoin
                // .revInclude(new Include("..."))
                .returnBundle(Bundle.class)
                .execute();

        // 2. Conversion en JSON String
        String jsonString = ctx.newJsonParser().encodeResourceToString(bundle);

        // 3. Sauvegarde en base locale
        FhirBundleEntity entity = new FhirBundleEntity();
        entity.setPatientId(patientId);
        entity.setRawJson(jsonString);
        repository.save(entity);

        return "Données synchronisées pour le patient " + patientId;
    }

}
