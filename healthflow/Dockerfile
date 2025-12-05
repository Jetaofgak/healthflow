# Utiliser une image Java légère
FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
# On copie le JAR généré (vérifie le nom dans ton dossier target/)
COPY target/*.jar app.jar
# Port exposé
EXPOSE 8081
# Commande de lancement
ENTRYPOINT ["java", "-jar", "app.jar"]
