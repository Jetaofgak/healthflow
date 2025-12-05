# --- Étape 1 : Build (Compilation) ---
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

# Copier le pom.xml et télécharger les dépendances (cache)
COPY pom.xml .
# Cette ligne télécharge les dépendances sans copier tout le code (optimisation)
RUN mvn dependency:go-offline

# Copier le code source
COPY src ./src

# Compiler le projet (crée le dossier target/)
RUN mvn clean package -DskipTests

# --- Étape 2 : Run (Exécution) ---
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Copier le jar généré depuis l'étape de build
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
