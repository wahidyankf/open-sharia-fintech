import path from "path";
import { useState } from "react";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { expect, vi } from "vitest";
import { createActor, type Actor } from "xstate";
import { appMachine } from "@/contexts/app-shell/presentation/app-machine";
import type { JournalRuntime } from "@/contexts/journal/application";
import { ReadingLogger } from "@/contexts/app-shell/presentation/components/loggers/reading-logger";
import { LearningLogger } from "@/contexts/app-shell/presentation/components/loggers/learning-logger";
import { MealLogger } from "@/contexts/app-shell/presentation/components/loggers/meal-logger";
import { FocusLogger } from "@/contexts/app-shell/presentation/components/loggers/focus-logger";
import { CustomEntryLogger } from "@/contexts/app-shell/presentation/components/loggers/custom-entry-logger";

type LoggerKind = "reading" | "learning" | "meal" | "focus" | "custom";
let runPromise: ReturnType<typeof vi.fn> = vi.fn().mockResolvedValue(undefined);

function LoggerHost({ kind }: { kind: LoggerKind }) {
  const [open, setOpen] = useState(true);
  const props = {
    isOpen: open,
    onClose: () => setOpen(false),
    onSaved: () => setOpen(false),
    runtime: { runPromise } as unknown as JournalRuntime,
  };
  if (kind === "reading") return <ReadingLogger {...props} />;
  if (kind === "learning") return <LearningLogger {...props} />;
  if (kind === "meal") return <MealLogger {...props} />;
  if (kind === "focus") return <FocusLogger {...props} />;
  return <CustomEntryLogger {...props} />;
}

function makeActor() {
  return createActor(appMachine, { input: { initialDarkMode: false, initialTab: "home" } }).start();
}

const feature = await loadFeature(
  path.resolve(
    __dirname,
    "../../../../../../specs/apps/organiclever/app-web/behaviours/app-shell/entry-loggers.feature",
  ),
);

describeFeature(feature, ({ Scenario, AfterEachScenario }) => {
  let actor: Actor<typeof appMachine>;

  AfterEachScenario(() => {
    cleanup();
    runPromise = vi.fn().mockResolvedValue(undefined);
  });

  Scenario("Open Add Entry sheet", ({ Given, When, Then }) => {
    Given("the app shell is visible", () => {
      actor = makeActor();
    });
    When("the user taps the FAB", () => actor.send({ type: "OPEN_ADD_ENTRY" }));
    Then("the Add Entry sheet is open with all entry kinds", () => {
      expect(actor.getSnapshot().matches("addEntry")).toBe(true);
    });
  });

  Scenario("Close Add Entry sheet", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user closes the Add Entry sheet", () => actor.send({ type: "CLOSE_ADD_ENTRY" }));
    Then("the Add Entry sheet is closed", () => expect(actor.getSnapshot().matches("none")).toBe(true));
  });

  Scenario("Open reading logger from Add Entry sheet", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user selects the Reading entry kind", () => actor.send({ type: "OPEN_LOGGER", kind: "reading" }));
    Then("the reading logger is open", () => {
      expect(actor.getSnapshot().context.loggerKind).toBe("reading");
    });
  });

  Scenario("Log a reading entry", ({ Given, When, Then, And }) => {
    Given("the user has opened the reading logger", () => {
      render(<LoggerHost kind="reading" />);
    });
    When('the user enters title "Atomic Habits"', () => {
      fireEvent.change(screen.getByPlaceholderText("e.g. Thinking Fast and Slow"), {
        target: { value: "Atomic Habits" },
      });
    });
    And("the user saves the entry", () => {
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
    });
    Then("the entry is saved and the logger closes", () => {
      expect(runPromise).toHaveBeenCalledTimes(1);
      expect(screen.queryByText("Log reading")).not.toBeInTheDocument();
    });
  });

  Scenario("Reading logger save is disabled without title", ({ Given, When, Then }) => {
    Given("the user has opened the reading logger", () => {
      render(<LoggerHost kind="reading" />);
    });
    When("the user has not entered a title", () => {
      fireEvent.change(screen.getByPlaceholderText("e.g. Thinking Fast and Slow"), { target: { value: "" } });
    });
    Then("the save button is disabled", () => expect(screen.getByRole("button", { name: "Save" })).toBeDisabled());
  });

  Scenario("Open learning logger from Add Entry sheet", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user selects the Learning entry kind", () => actor.send({ type: "OPEN_LOGGER", kind: "learning" }));
    Then("the learning logger is open", () => expect(actor.getSnapshot().context.loggerKind).toBe("learning"));
  });

  Scenario("Log a learning entry", ({ Given, When, Then, And }) => {
    Given("the user has opened the learning logger", () => {
      render(<LoggerHost kind="learning" />);
    });
    When('the user enters subject "TypeScript generics"', () => {
      fireEvent.change(screen.getByPlaceholderText(/React hooks/), { target: { value: "TypeScript generics" } });
    });
    And("the user saves the entry", () => {
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
    });
    Then("the entry is saved and the logger closes", () => {
      expect(runPromise).toHaveBeenCalledTimes(1);
      expect(screen.queryByText("Log learning")).not.toBeInTheDocument();
    });
  });

  Scenario("Open meal logger from Add Entry sheet", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user selects the Meal entry kind", () => actor.send({ type: "OPEN_LOGGER", kind: "meal" }));
    Then("the meal logger is open", () => expect(actor.getSnapshot().context.loggerKind).toBe("meal"));
  });

  Scenario("Log a meal entry", ({ Given, When, Then, And }) => {
    Given("the user has opened the meal logger", () => {
      render(<LoggerHost kind="meal" />);
    });
    When('the user enters meal name "Oatmeal with berries"', () => {
      fireEvent.change(screen.getByPlaceholderText(/Oatmeal with berries/), {
        target: { value: "Oatmeal with berries" },
      });
    });
    And("the user saves the entry", () => {
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
    });
    Then("the entry is saved and the logger closes", () => {
      expect(runPromise).toHaveBeenCalledTimes(1);
      expect(screen.queryByText("Log meal")).not.toBeInTheDocument();
    });
  });

  Scenario("Open focus logger from Add Entry sheet", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user selects the Focus entry kind", () => actor.send({ type: "OPEN_LOGGER", kind: "focus" }));
    Then("the focus logger is open", () => expect(actor.getSnapshot().context.loggerKind).toBe("focus"));
  });

  Scenario("Log a focus entry", ({ Given, When, Then, And }) => {
    Given("the user has opened the focus logger", () => {
      render(<LoggerHost kind="focus" />);
    });
    When("the user selects the 25min preset", () => {
      fireEvent.click(screen.getByRole("button", { name: "25" }));
    });
    And("the user saves the entry", () => {
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
    });
    Then("the entry is saved and the logger closes", () => {
      expect(runPromise).toHaveBeenCalledTimes(1);
      expect(screen.queryByText("Log focus session")).not.toBeInTheDocument();
    });
  });

  Scenario("Focus logger save requires task or duration", ({ Given, When, Then }) => {
    Given("the user has opened the focus logger", () => {
      render(<LoggerHost kind="focus" />);
    });
    When("the user has not entered task or duration", () => {
      fireEvent.change(screen.getByPlaceholderText(/Feature design/), { target: { value: "" } });
      fireEvent.change(screen.getByPlaceholderText("or enter custom minutes"), { target: { value: "" } });
    });
    Then("the save button is disabled", () => expect(screen.getByRole("button", { name: "Save" })).toBeDisabled());
  });

  Scenario("Open custom entry logger", ({ Given, When, Then }) => {
    Given("the user has opened the Add Entry sheet", () => {
      actor = makeActor();
      actor.send({ type: "OPEN_ADD_ENTRY" });
    });
    When("the user selects the custom entry kind", () => actor.send({ type: "OPEN_CUSTOM_LOGGER" }));
    Then("the custom entry logger is open", () => expect(actor.getSnapshot().matches("customLoggerOpen")).toBe(true));
  });

  Scenario("Log a custom entry", ({ Given, When, Then, And }) => {
    Given("the user has opened the custom entry logger", () => {
      render(<LoggerHost kind="custom" />);
    });
    When('the user enters custom entry name "Evening walk"', () => {
      fireEvent.change(screen.getByPlaceholderText(/Evening walk/), { target: { value: "Evening walk" } });
    });
    And("the user saves the custom entry", () => {
      fireEvent.click(screen.getByRole("button", { name: "Save" }));
    });
    Then("the custom entry is saved and the logger closes", async () => {
      await waitFor(() => expect(runPromise).toHaveBeenCalledTimes(1));
      await waitFor(() => expect(screen.queryByText("New custom entry")).not.toBeInTheDocument());
    });
  });
});
