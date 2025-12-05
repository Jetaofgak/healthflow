FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

# On utilise le chemin complet depuis la racine du repo
COPY healthflow/pom.xml .
# (Optionnel, on peut sauter le go-offline pour tester vite)

COPY healthflow/src ./src

# Il faut exécuter maven là où est le pom
RUN mvn -f pom.xml clean package -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
