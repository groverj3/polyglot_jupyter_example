system("mkdir polyglot_jupyter_example_r")

list.files()

# Confirm that only the tidyverse packages and their dependencies are here

installed.packages() |> rownames()

# This tells you the status of packages in the lockfile vs what's used

renv::status()

library(tidyverse)

# Load the same test dataset

titanic <- read_csv("test_data/titanic.csv")

titanic |> head()

titanic |> summary()

# Make a copy for further use

titanic_survival <- titanic

# Convert the survived to boolean

titanic_survival$Survived <- titanic_survival$Survived |> as.logical()

# Perform the same "analysis" as in Python

titanic_survival <- titanic_survival |>
    count(Pclass, Survived)

titanic_survival

titanic_survival |> head()

# Add a column for percent survival

titanic_survival <- titanic_survival |>
    group_by(Pclass) |>
    mutate(
        Percentage = (n/sum(n) * 100)
    ) |>
    ungroup()

titanic_survival

# Save as a csv

titanic_survival |> write_csv("polyglot_jupyter_example_r/titanic_survival.csv")

# Get survival rate by class and sex

titanic_survival_2 <- titanic |>
    mutate(
        Survived = as.logical(Survived)
    ) |>
    group_by(Pclass, Survived, Sex) |>
    count() |>
    group_by(Pclass, Sex) |>
    mutate(
        Percentage = (n/sum(n) * 100)
    ) |>
    ungroup()

titanic_survival_2

# Make a bar plot of survival rate by class and sex

titanic_survival_2 |> filter(Survived) |>
    ggplot(aes(
        x = Pclass,
        y = Percentage,
        fill = Sex
    )) +
    geom_col(
        position = "dodge"
    ) +
    scale_fill_brewer(
        type = "qual",
        palette = "Dark2"
    ) +
    labs(
        title = "Titanic Survival Rate",
        x = "Passenger Class"
    ) +
    theme_bw() 

# Plot the fare by class and age

titanic |>
    ggplot(aes(
        x = Age,
        y = Fare,
        color = as.character(Pclass)
    )) +
    geom_point() +
    scale_color_brewer(
        type = "qual",
        palette = "Dark2"
    ) +
    labs(
        color = "Passenger Class"
    ) +
    theme_bw()

# To make the swarmplot we need ggbeeswarm

library(ggbeeswarm)

# Combination violin and swarmplot, just like the python example
# Swarmplots are a separate package, this is an approximation with a dotplot instead

titanic |>
    ggplot(aes(
        y = as.character(Pclass),
        x = Age
    )) +
    geom_violin(
        fill = "lightgrey",
        trim = FALSE
    ) +
    geom_beeswarm(
        color = "dodgerblue3"
    ) +
    labs(
        y = "Passenger Class"
    ) +
    theme_bw()

# Update the lock file

renv::snapshot(type = "all")

# I also export the notebook as a .r script so it can be run without jupyter and .html so non-coders can view it

system("jupyter nbconvert --to script --output-dir ./polyglot_jupyter_example_r/ polyglot_jupyter_example_r.ipynb")
system("jupyter nbconvert --to html --output-dir ./polyglot_jupyter_example_r/ polyglot_jupyter_example_r.ipynb")

sessionInfo()
