import { expect, type Page } from "@playwright/test";
import { appPath } from "./_app-shell";

interface RoutineSetup {
  readonly name: string;
  readonly exerciseName?: string;
  readonly rest?: "30s" | "60s" | "90s";
}

/** Establishes routine state through the same UI and persistence path a user exercises. */
export async function createRoutine(page: Page, setup: RoutineSetup): Promise<void> {
  await page.goto(appPath("home"));
  await page.getByRole("button", { name: "New" }).click();
  await expect(page.getByRole("heading", { name: "New routine" })).toBeVisible();

  await page.getByLabel("Routine name").fill(setup.name);
  if (setup.exerciseName) {
    await page.getByRole("button", { name: "Add exercise to Main" }).click();
    await page.getByRole("button", { name: "Expand exercise" }).click();
    await page.getByLabel("Exercise name").fill(setup.exerciseName);
    if (setup.rest) {
      await page.getByRole("button", { name: setup.rest, exact: true }).click();
    }
  }

  await page.getByRole("button", { name: "Save", exact: true }).click();
  await expect(page).toHaveURL(/\/app\/home$/);
  await expect(page.getByText(setup.name, { exact: true })).toBeVisible();
}
