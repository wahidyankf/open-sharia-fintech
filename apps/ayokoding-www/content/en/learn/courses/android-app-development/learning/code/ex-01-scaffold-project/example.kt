// app/build.gradle.kts: Android application + Compose enabled.
plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android { namespace = "com.example.focus"; compileSdk = 36
  defaultConfig { applicationId = "com.example.focus"; minSdk = 24; targetSdk = 36 }
  buildFeatures { compose = true }
}
dependencies { implementation(platform(libs.androidx.compose.bom)); implementation(libs.androidx.activity.compose) }
