class MainActivity : ComponentActivity() {
  override fun onStart() { super.onStart(); Log.d("Focus", "visible") }
  override fun onStop() { Log.d("Focus", "no longer visible"); super.onStop() }
}
