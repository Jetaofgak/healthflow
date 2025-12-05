# Utiliser une image Java légère
FROM openjdk:25-jdk-slim
WORKDIR /app
# On copie le JAR généré (vérifie le nom dans ton dossier target/)
COPY target/*.jar app.jar
# Port exposé
EXPOSE 8081
# Commande de lancement
ENTRYPOINT ["java", "-jar", "app.jar"]
