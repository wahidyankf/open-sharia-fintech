using System.Windows.Automation;

namespace UiAutomationExample;

public static class UiAutomationSmoke
{
    public static AutomationElement FindSaveButton(AutomationElement window) =>
        window.FindFirst(
            TreeScope.Descendants,
            new AndCondition(
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Button),
                new PropertyCondition(AutomationElement.NameProperty, "Save")
            )
        ) ?? throw new InvalidOperationException("Save button was not found.");
}
