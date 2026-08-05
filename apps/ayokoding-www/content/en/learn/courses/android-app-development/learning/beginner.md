---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish Android project, platform, and Compose fundamentals. They move from the manifest and activity lifecycle into declarative UI, observable state, Material components, and efficient lists.

### Example 1: Scaffold a Project

_ex-01 · exercises co-01_

Scaffold a Project isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-01-scaffold-project/example.kt`**

```kotlin
// app/build.gradle.kts: Android application + Compose enabled.
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android { namespace = "com.example.focus"; compileSdk = 36
  defaultConfig { applicationId = "com.example.focus"; minSdk = 24; targetSdk = 36 }
  buildFeatures { compose = true }
}
dependencies { implementation(platform(libs.androidx.compose.bom)); implementation(libs.androidx.activity.compose) }

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Scaffold a Project keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 2: Declare the Launcher Activity

_ex-02 · exercises co-02_

Declare the Launcher Activity isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-02-manifest-declare-activity/example.kt`**

```kotlin
<!-- AndroidManifest.xml -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"><application android:theme="@style/Theme.Focus"><activity android:name=".MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN" /><category android:name="android.intent.category.LAUNCHER" /></intent-filter></activity></application></manifest>

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Declare the Launcher Activity keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 3: Declare Internet Permission

_ex-03 · exercises co-02_

Declare Internet Permission isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-03-manifest-permission/example.kt`**

```kotlin
<!-- AndroidManifest.xml: normal permission declared at install time. -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET" /><application android:label="@string/app_name" /></manifest>

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Declare Internet Permission keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 4: Create an Activity and Set Content

_ex-04 · exercises co-03, co-05_

Create an Activity and Set Content isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-04-activity-oncreate/example.kt`**

```kotlin
class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContent { FocusTheme { FocusApp() } }
  }
}

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Create an Activity and Set Content keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 5: Log the Activity Lifecycle

_ex-05 · exercises co-03_

Log the Activity Lifecycle isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-05-lifecycle-logging/example.kt`**

```kotlin
class MainActivity : ComponentActivity() {
  override fun onStart() { super.onStart(); Log.d("Focus", "visible") }
  override fun onStop() { Log.d("Focus", "no longer visible"); super.onStop() }
}

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Log the Activity Lifecycle keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 6: Start an Explicit Intent

_ex-06 · exercises co-04_

Start an Explicit Intent isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-06-explicit-intent/example.kt`**

```kotlin
fun Context.openNote(noteId: String) {
  startActivity(Intent(this, NoteDetailActivity::class.java)
    .putExtra(NoteDetailActivity.NOTE_ID, noteId))
}

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Start an Explicit Intent keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 7: Start an Implicit Intent

_ex-07 · exercises co-04_

Start an Implicit Intent isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-07-implicit-intent/example.kt`**

```kotlin
fun Context.shareNote(text: String) {
  startActivity(Intent.createChooser(
    Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT, text), "Share note"))
}

```

**Run**: `./gradlew assembleDebug` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Start an Implicit Intent keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 8: Render a Hello Composable

_ex-08 · exercises co-05_

Render a Hello Composable isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-08-composable-hello/example.kt`**

```kotlin
@Composable
fun Greeting(name: String) {
  Text(text = "Hello, $name")
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render a Hello Composable keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 9: Host a Compose Tree

_ex-09 · exercises co-05_

Host a Compose Tree isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-09-setcontent-tree/example.kt`**

```kotlin
class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContent { MaterialTheme { Surface { Greeting("Ada") } } }
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Host a Compose Tree keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 10: Pass Text as Data

_ex-10 · exercises co-05_

Pass Text as Data isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-10-text-composable/example.kt`**

```kotlin
@Composable
fun NoteTitle(title: String, modifier: Modifier = Modifier) {
  Text(text = title, modifier = modifier, style = MaterialTheme.typography.titleMedium)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Pass Text as Data keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 11: Recompose from State

_ex-11 · exercises co-06_

Recompose from State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-11-recomposition-on-state/example.kt`**

```kotlin
@Composable
fun TapCount() {
  var taps by remember { mutableIntStateOf(0) }
  Button(onClick = { taps++ }) { Text("Tapped $taps times") }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Recompose from State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 12: Remember Mutable State

_ex-12 · exercises co-07_

Remember Mutable State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-12-remember-mutablestateof/example.kt`**

```kotlin
@Composable
fun EditableLabel() {
  var label by remember { mutableStateOf("") }
  OutlinedTextField(value = label, onValueChange = { label = it }, label = { Text("Label") })
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Remember Mutable State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 13: Increment a State Counter

_ex-13 · exercises co-07_

Increment a State Counter isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-13-state-counter/example.kt`**

```kotlin
@Composable
fun Counter() {
  var count by remember { mutableIntStateOf(0) }
  Button(onClick = { count++ }) { Text("Count: $count") }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Increment a State Counter keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 14: Hoist Counter State

_ex-14 · exercises co-08_

Hoist Counter State isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-14-hoisted-state/example.kt`**

```kotlin
@Composable
fun Counter(value: Int, onIncrement: () -> Unit) {
  Button(onClick = onIncrement) { Text("Count: $value") }
}
@Composable
fun CounterOwner() {
  var value by remember { mutableIntStateOf(0) }
  Counter(value, onIncrement = { value++ })
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Hoist Counter State keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 15: Reuse a Stateless Counter

_ex-15 · exercises co-08_

Reuse a Stateless Counter isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-15-stateless-reuse/example.kt`**

```kotlin
@Composable
fun QuantityStepper(value: Int, onValueChange: (Int) -> Unit) {
  Row { Button(onClick = { onValueChange(value - 1) }) { Text("-") }
    Text("$value"); Button(onClick = { onValueChange(value + 1) }) { Text("+") } }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Reuse a Stateless Counter keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 16: Apply Modifier Padding

_ex-16 · exercises co-09_

Apply Modifier Padding isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-16-modifier-padding/example.kt`**

```kotlin
@Composable
fun PaddedTitle() {
  Text("Focus notes", modifier = Modifier.padding(16.dp))
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Apply Modifier Padding keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 17: Chain Modifiers

_ex-17 · exercises co-09_

Chain Modifiers isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-17-modifier-chain/example.kt`**

```kotlin
@Composable
fun SelectedNote(title: String) {
  Text(title, Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.secondaryContainer)
    .padding(horizontal = 16.dp, vertical = 12.dp))
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Chain Modifiers keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 18: Add a Preview

_ex-18 · exercises co-10_

Add a Preview isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-18-preview-annotation/example.kt`**

```kotlin
@Preview(showBackground = true)
@Composable
private fun NoteTitlePreview() {
  MaterialTheme { NoteTitle("Plan release") }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Add a Preview keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 19: Lay Out a Column

_ex-19 · exercises co-11_

Lay Out a Column isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-19-column-layout/example.kt`**

```kotlin
@Composable
fun NoteSummary(title: String, body: String) {
  Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
    Text(title, style = MaterialTheme.typography.titleMedium)
    Text(body, style = MaterialTheme.typography.bodyMedium)
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Lay Out a Column keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 20: Lay Out a Row

_ex-20 · exercises co-11_

Lay Out a Row isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-20-row-layout/example.kt`**

```kotlin
@Composable
fun NoteMetadata(updated: String) {
  Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
    Icon(Icons.Outlined.Schedule, contentDescription = null); Text("Updated $updated")
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Lay Out a Row keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 21: Overlay Content in a Box

_ex-21 · exercises co-11_

Overlay Content in a Box isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-21-box-overlay/example.kt`**

```kotlin
@Composable
fun SyncBadge(syncing: Boolean) {
  Box {
    Icon(Icons.Outlined.Cloud, contentDescription = "Cloud sync")
    if (syncing) CircularProgressIndicator(Modifier.align(Alignment.BottomEnd).size(12.dp))
  }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Overlay Content in a Box keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 22: Use Scaffold and Top App Bar

_ex-22 · exercises co-12_

Use Scaffold and Top App Bar isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-22-scaffold-topbar/example.kt`**

```kotlin
@Composable
fun NotesScaffold(content: @Composable (PaddingValues) -> Unit) {
  Scaffold(topBar = { TopAppBar(title = { Text("Focus notes") }) }, content = content)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Use Scaffold and Top App Bar keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 23: Handle a Material Button Click

_ex-23 · exercises co-12_

Handle a Material Button Click isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-23-button-onclick/example.kt`**

```kotlin
@Composable
fun RetryButton(onRetry: () -> Unit) {
  Button(onClick = onRetry) { Text("Retry sync") }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Handle a Material Button Click keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 24: Bind an Outlined Text Field

_ex-24 · exercises co-12_

Bind an Outlined Text Field isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-24-textfield-input/example.kt`**

```kotlin
@Composable
fun SearchField(query: String, onQueryChange: (String) -> Unit) {
  OutlinedTextField(value = query, onValueChange = onQueryChange, label = { Text("Search notes") }, singleLine = true)
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Bind an Outlined Text Field keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 25: Render a Lazy Column

_ex-25 · exercises co-13_

Render a Lazy Column isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-25-lazycolumn-list/example.kt`**

```kotlin
@Composable
fun NoteList(notes: List<String>) {
  LazyColumn { items(notes, key = { it }) { title -> Text(title, Modifier.padding(16.dp)) } }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render a Lazy Column keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.

### Example 26: Render List Items

_ex-26 · exercises co-13_

Render List Items isolates one production decision in a deliberately small Android slice. Read the
annotations first, then place the artifact in the Compose app module and change one input to see
which state and UI responsibility changes with it.

**`learning/code/ex-26-lazycolumn-items/example.kt`**

```kotlin
data class Note(val id: String, val title: String)
@Composable
fun NoteRows(notes: List<Note>, onOpen: (String) -> Unit) {
  LazyColumn { items(notes, key = { it.id }) { note ->
    ListItem(headlineContent = { Text(note.title) }, modifier = Modifier.clickable { onOpen(note.id) })
  } }
}

```

**Run**: `./gradlew test` from the Android project root.

**Expected observation**: the example compiles in its intended Android module and makes its state,
event, or platform boundary explicit rather than hiding it in a callback.

**Key takeaway**: Render List Items keeps the platform concern at a named boundary so the UI can remain a
predictable function of inputs and state.

**Why it matters**: Android can recreate a screen, cancel work, deny a permission, or deliver a
network failure at any point. A small, explicit slice makes that event observable and testable;
scaling the same discipline across a feature prevents state from being duplicated between UI,
platform callbacks, and data sources.
