// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'schema.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$Health {

/// Always "ok" when the service is live.
 String get status;
/// Create a copy of Health
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$HealthCopyWith<Health> get copyWith => _$HealthCopyWithImpl<Health>(this as Health, _$identity);

  /// Serializes this Health to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Health&&(identical(other.status, status) || other.status == status));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status);

@override
String toString() {
  return 'Health(status: $status)';
}


}

/// @nodoc
abstract mixin class $HealthCopyWith<$Res>  {
  factory $HealthCopyWith(Health value, $Res Function(Health) _then) = _$HealthCopyWithImpl;
@useResult
$Res call({
 String status
});




}
/// @nodoc
class _$HealthCopyWithImpl<$Res>
    implements $HealthCopyWith<$Res> {
  _$HealthCopyWithImpl(this._self, this._then);

  final Health _self;
  final $Res Function(Health) _then;

/// Create a copy of Health
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? status = null,}) {
  return _then(_self.copyWith(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [Health].
extension HealthPatterns on Health {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _Health value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _Health() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _Health value)  $default,){
final _that = this;
switch (_that) {
case _Health():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _Health value)?  $default,){
final _that = this;
switch (_that) {
case _Health() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String status)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _Health() when $default != null:
return $default(_that.status);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String status)  $default,) {final _that = this;
switch (_that) {
case _Health():
return $default(_that.status);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String status)?  $default,) {final _that = this;
switch (_that) {
case _Health() when $default != null:
return $default(_that.status);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _Health extends Health {
  const _Health({required this.status}): super._();
  factory _Health.fromJson(Map<String, dynamic> json) => _$HealthFromJson(json);

/// Always "ok" when the service is live.
@override final  String status;

/// Create a copy of Health
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$HealthCopyWith<_Health> get copyWith => __$HealthCopyWithImpl<_Health>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$HealthToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _Health&&(identical(other.status, status) || other.status == status));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status);

@override
String toString() {
  return 'Health(status: $status)';
}


}

/// @nodoc
abstract mixin class _$HealthCopyWith<$Res> implements $HealthCopyWith<$Res> {
  factory _$HealthCopyWith(_Health value, $Res Function(_Health) _then) = __$HealthCopyWithImpl;
@override @useResult
$Res call({
 String status
});




}
/// @nodoc
class __$HealthCopyWithImpl<$Res>
    implements _$HealthCopyWith<$Res> {
  __$HealthCopyWithImpl(this._self, this._then);

  final _Health _self;
  final $Res Function(_Health) _then;

/// Create a copy of Health
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? status = null,}) {
  return _then(_Health(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$ReadinessReady {

/// Fixed readiness status.
 String get status;/// Safe readiness component states.
 ReadinessReadyComponents get components;
/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ReadinessReadyCopyWith<ReadinessReady> get copyWith => _$ReadinessReadyCopyWithImpl<ReadinessReady>(this as ReadinessReady, _$identity);

  /// Serializes this ReadinessReady to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ReadinessReady&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'ReadinessReady(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class $ReadinessReadyCopyWith<$Res>  {
  factory $ReadinessReadyCopyWith(ReadinessReady value, $Res Function(ReadinessReady) _then) = _$ReadinessReadyCopyWithImpl;
@useResult
$Res call({
 String status, ReadinessReadyComponents components
});


$ReadinessReadyComponentsCopyWith<$Res> get components;

}
/// @nodoc
class _$ReadinessReadyCopyWithImpl<$Res>
    implements $ReadinessReadyCopyWith<$Res> {
  _$ReadinessReadyCopyWithImpl(this._self, this._then);

  final ReadinessReady _self;
  final $Res Function(ReadinessReady) _then;

/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? status = null,Object? components = null,}) {
  return _then(_self.copyWith(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as ReadinessReadyComponents,
  ));
}
/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReadinessReadyComponentsCopyWith<$Res> get components {

  return $ReadinessReadyComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// Adds pattern-matching-related methods to [ReadinessReady].
extension ReadinessReadyPatterns on ReadinessReady {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ReadinessReady value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ReadinessReady() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ReadinessReady value)  $default,){
final _that = this;
switch (_that) {
case _ReadinessReady():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ReadinessReady value)?  $default,){
final _that = this;
switch (_that) {
case _ReadinessReady() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String status,  ReadinessReadyComponents components)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ReadinessReady() when $default != null:
return $default(_that.status,_that.components);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String status,  ReadinessReadyComponents components)  $default,) {final _that = this;
switch (_that) {
case _ReadinessReady():
return $default(_that.status,_that.components);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String status,  ReadinessReadyComponents components)?  $default,) {final _that = this;
switch (_that) {
case _ReadinessReady() when $default != null:
return $default(_that.status,_that.components);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ReadinessReady extends ReadinessReady {
  const _ReadinessReady({required this.status, required this.components}): super._();
  factory _ReadinessReady.fromJson(Map<String, dynamic> json) => _$ReadinessReadyFromJson(json);

/// Fixed readiness status.
@override final  String status;
/// Safe readiness component states.
@override final  ReadinessReadyComponents components;

/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ReadinessReadyCopyWith<_ReadinessReady> get copyWith => __$ReadinessReadyCopyWithImpl<_ReadinessReady>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ReadinessReadyToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ReadinessReady&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'ReadinessReady(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class _$ReadinessReadyCopyWith<$Res> implements $ReadinessReadyCopyWith<$Res> {
  factory _$ReadinessReadyCopyWith(_ReadinessReady value, $Res Function(_ReadinessReady) _then) = __$ReadinessReadyCopyWithImpl;
@override @useResult
$Res call({
 String status, ReadinessReadyComponents components
});


@override $ReadinessReadyComponentsCopyWith<$Res> get components;

}
/// @nodoc
class __$ReadinessReadyCopyWithImpl<$Res>
    implements _$ReadinessReadyCopyWith<$Res> {
  __$ReadinessReadyCopyWithImpl(this._self, this._then);

  final _ReadinessReady _self;
  final $Res Function(_ReadinessReady) _then;

/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? status = null,Object? components = null,}) {
  return _then(_ReadinessReady(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as ReadinessReadyComponents,
  ));
}

/// Create a copy of ReadinessReady
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReadinessReadyComponentsCopyWith<$Res> get components {

  return $ReadinessReadyComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// @nodoc
mixin _$ReadinessReadyComponents {

/// Fixed database readiness state.
 String get database;/// Fixed schema readiness state.
 String get schema;
/// Create a copy of ReadinessReadyComponents
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ReadinessReadyComponentsCopyWith<ReadinessReadyComponents> get copyWith => _$ReadinessReadyComponentsCopyWithImpl<ReadinessReadyComponents>(this as ReadinessReadyComponents, _$identity);

  /// Serializes this ReadinessReadyComponents to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ReadinessReadyComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'ReadinessReadyComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class $ReadinessReadyComponentsCopyWith<$Res>  {
  factory $ReadinessReadyComponentsCopyWith(ReadinessReadyComponents value, $Res Function(ReadinessReadyComponents) _then) = _$ReadinessReadyComponentsCopyWithImpl;
@useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class _$ReadinessReadyComponentsCopyWithImpl<$Res>
    implements $ReadinessReadyComponentsCopyWith<$Res> {
  _$ReadinessReadyComponentsCopyWithImpl(this._self, this._then);

  final ReadinessReadyComponents _self;
  final $Res Function(ReadinessReadyComponents) _then;

/// Create a copy of ReadinessReadyComponents
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_self.copyWith(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [ReadinessReadyComponents].
extension ReadinessReadyComponentsPatterns on ReadinessReadyComponents {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ReadinessReadyComponents value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ReadinessReadyComponents() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ReadinessReadyComponents value)  $default,){
final _that = this;
switch (_that) {
case _ReadinessReadyComponents():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ReadinessReadyComponents value)?  $default,){
final _that = this;
switch (_that) {
case _ReadinessReadyComponents() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String database,  String schema)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ReadinessReadyComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String database,  String schema)  $default,) {final _that = this;
switch (_that) {
case _ReadinessReadyComponents():
return $default(_that.database,_that.schema);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String database,  String schema)?  $default,) {final _that = this;
switch (_that) {
case _ReadinessReadyComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ReadinessReadyComponents extends ReadinessReadyComponents {
  const _ReadinessReadyComponents({required this.database, required this.schema}): super._();
  factory _ReadinessReadyComponents.fromJson(Map<String, dynamic> json) => _$ReadinessReadyComponentsFromJson(json);

/// Fixed database readiness state.
@override final  String database;
/// Fixed schema readiness state.
@override final  String schema;

/// Create a copy of ReadinessReadyComponents
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ReadinessReadyComponentsCopyWith<_ReadinessReadyComponents> get copyWith => __$ReadinessReadyComponentsCopyWithImpl<_ReadinessReadyComponents>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ReadinessReadyComponentsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ReadinessReadyComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'ReadinessReadyComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class _$ReadinessReadyComponentsCopyWith<$Res> implements $ReadinessReadyComponentsCopyWith<$Res> {
  factory _$ReadinessReadyComponentsCopyWith(_ReadinessReadyComponents value, $Res Function(_ReadinessReadyComponents) _then) = __$ReadinessReadyComponentsCopyWithImpl;
@override @useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class __$ReadinessReadyComponentsCopyWithImpl<$Res>
    implements _$ReadinessReadyComponentsCopyWith<$Res> {
  __$ReadinessReadyComponentsCopyWithImpl(this._self, this._then);

  final _ReadinessReadyComponents _self;
  final $Res Function(_ReadinessReadyComponents) _then;

/// Create a copy of ReadinessReadyComponents
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_ReadinessReadyComponents(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$ReadinessUnavailable {

/// Fixed unavailable readiness status.
 String get status;/// Safe unavailable component states without operational detail.
 ReadinessUnavailableComponents get components;
/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ReadinessUnavailableCopyWith<ReadinessUnavailable> get copyWith => _$ReadinessUnavailableCopyWithImpl<ReadinessUnavailable>(this as ReadinessUnavailable, _$identity);

  /// Serializes this ReadinessUnavailable to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ReadinessUnavailable&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'ReadinessUnavailable(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class $ReadinessUnavailableCopyWith<$Res>  {
  factory $ReadinessUnavailableCopyWith(ReadinessUnavailable value, $Res Function(ReadinessUnavailable) _then) = _$ReadinessUnavailableCopyWithImpl;
@useResult
$Res call({
 String status, ReadinessUnavailableComponents components
});


$ReadinessUnavailableComponentsCopyWith<$Res> get components;

}
/// @nodoc
class _$ReadinessUnavailableCopyWithImpl<$Res>
    implements $ReadinessUnavailableCopyWith<$Res> {
  _$ReadinessUnavailableCopyWithImpl(this._self, this._then);

  final ReadinessUnavailable _self;
  final $Res Function(ReadinessUnavailable) _then;

/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? status = null,Object? components = null,}) {
  return _then(_self.copyWith(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as ReadinessUnavailableComponents,
  ));
}
/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReadinessUnavailableComponentsCopyWith<$Res> get components {

  return $ReadinessUnavailableComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// Adds pattern-matching-related methods to [ReadinessUnavailable].
extension ReadinessUnavailablePatterns on ReadinessUnavailable {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ReadinessUnavailable value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ReadinessUnavailable() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ReadinessUnavailable value)  $default,){
final _that = this;
switch (_that) {
case _ReadinessUnavailable():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ReadinessUnavailable value)?  $default,){
final _that = this;
switch (_that) {
case _ReadinessUnavailable() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String status,  ReadinessUnavailableComponents components)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ReadinessUnavailable() when $default != null:
return $default(_that.status,_that.components);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String status,  ReadinessUnavailableComponents components)  $default,) {final _that = this;
switch (_that) {
case _ReadinessUnavailable():
return $default(_that.status,_that.components);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String status,  ReadinessUnavailableComponents components)?  $default,) {final _that = this;
switch (_that) {
case _ReadinessUnavailable() when $default != null:
return $default(_that.status,_that.components);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ReadinessUnavailable extends ReadinessUnavailable {
  const _ReadinessUnavailable({required this.status, required this.components}): super._();
  factory _ReadinessUnavailable.fromJson(Map<String, dynamic> json) => _$ReadinessUnavailableFromJson(json);

/// Fixed unavailable readiness status.
@override final  String status;
/// Safe unavailable component states without operational detail.
@override final  ReadinessUnavailableComponents components;

/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ReadinessUnavailableCopyWith<_ReadinessUnavailable> get copyWith => __$ReadinessUnavailableCopyWithImpl<_ReadinessUnavailable>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ReadinessUnavailableToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ReadinessUnavailable&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'ReadinessUnavailable(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class _$ReadinessUnavailableCopyWith<$Res> implements $ReadinessUnavailableCopyWith<$Res> {
  factory _$ReadinessUnavailableCopyWith(_ReadinessUnavailable value, $Res Function(_ReadinessUnavailable) _then) = __$ReadinessUnavailableCopyWithImpl;
@override @useResult
$Res call({
 String status, ReadinessUnavailableComponents components
});


@override $ReadinessUnavailableComponentsCopyWith<$Res> get components;

}
/// @nodoc
class __$ReadinessUnavailableCopyWithImpl<$Res>
    implements _$ReadinessUnavailableCopyWith<$Res> {
  __$ReadinessUnavailableCopyWithImpl(this._self, this._then);

  final _ReadinessUnavailable _self;
  final $Res Function(_ReadinessUnavailable) _then;

/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? status = null,Object? components = null,}) {
  return _then(_ReadinessUnavailable(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as ReadinessUnavailableComponents,
  ));
}

/// Create a copy of ReadinessUnavailable
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$ReadinessUnavailableComponentsCopyWith<$Res> get components {

  return $ReadinessUnavailableComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// @nodoc
mixin _$ReadinessUnavailableComponents {

/// Fixed unavailable database state.
 String get database;/// Fixed unknown schema state.
 String get schema;
/// Create a copy of ReadinessUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ReadinessUnavailableComponentsCopyWith<ReadinessUnavailableComponents> get copyWith => _$ReadinessUnavailableComponentsCopyWithImpl<ReadinessUnavailableComponents>(this as ReadinessUnavailableComponents, _$identity);

  /// Serializes this ReadinessUnavailableComponents to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ReadinessUnavailableComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'ReadinessUnavailableComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class $ReadinessUnavailableComponentsCopyWith<$Res>  {
  factory $ReadinessUnavailableComponentsCopyWith(ReadinessUnavailableComponents value, $Res Function(ReadinessUnavailableComponents) _then) = _$ReadinessUnavailableComponentsCopyWithImpl;
@useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class _$ReadinessUnavailableComponentsCopyWithImpl<$Res>
    implements $ReadinessUnavailableComponentsCopyWith<$Res> {
  _$ReadinessUnavailableComponentsCopyWithImpl(this._self, this._then);

  final ReadinessUnavailableComponents _self;
  final $Res Function(ReadinessUnavailableComponents) _then;

/// Create a copy of ReadinessUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_self.copyWith(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [ReadinessUnavailableComponents].
extension ReadinessUnavailableComponentsPatterns on ReadinessUnavailableComponents {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ReadinessUnavailableComponents value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ReadinessUnavailableComponents value)  $default,){
final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ReadinessUnavailableComponents value)?  $default,){
final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String database,  String schema)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String database,  String schema)  $default,) {final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents():
return $default(_that.database,_that.schema);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String database,  String schema)?  $default,) {final _that = this;
switch (_that) {
case _ReadinessUnavailableComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ReadinessUnavailableComponents extends ReadinessUnavailableComponents {
  const _ReadinessUnavailableComponents({required this.database, required this.schema}): super._();
  factory _ReadinessUnavailableComponents.fromJson(Map<String, dynamic> json) => _$ReadinessUnavailableComponentsFromJson(json);

/// Fixed unavailable database state.
@override final  String database;
/// Fixed unknown schema state.
@override final  String schema;

/// Create a copy of ReadinessUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ReadinessUnavailableComponentsCopyWith<_ReadinessUnavailableComponents> get copyWith => __$ReadinessUnavailableComponentsCopyWithImpl<_ReadinessUnavailableComponents>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ReadinessUnavailableComponentsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ReadinessUnavailableComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'ReadinessUnavailableComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class _$ReadinessUnavailableComponentsCopyWith<$Res> implements $ReadinessUnavailableComponentsCopyWith<$Res> {
  factory _$ReadinessUnavailableComponentsCopyWith(_ReadinessUnavailableComponents value, $Res Function(_ReadinessUnavailableComponents) _then) = __$ReadinessUnavailableComponentsCopyWithImpl;
@override @useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class __$ReadinessUnavailableComponentsCopyWithImpl<$Res>
    implements _$ReadinessUnavailableComponentsCopyWith<$Res> {
  __$ReadinessUnavailableComponentsCopyWithImpl(this._self, this._then);

  final _ReadinessUnavailableComponents _self;
  final $Res Function(_ReadinessUnavailableComponents) _then;

/// Create a copy of ReadinessUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_ReadinessUnavailableComponents(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$DiagnosticsReady {

/// No Description
 String get status;/// No Description
 String get version;/// Whole elapsed seconds since the service process started, rounded down.
 int get uptimeSeconds;/// Current UTC server time in RFC 3339 form.
 String get serverTimeUtc;/// Fixed named readiness component states for a ready snapshot.
 DiagnosticsReadyComponents get components;
/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DiagnosticsReadyCopyWith<DiagnosticsReady> get copyWith => _$DiagnosticsReadyCopyWithImpl<DiagnosticsReady>(this as DiagnosticsReady, _$identity);

  /// Serializes this DiagnosticsReady to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DiagnosticsReady&&(identical(other.status, status) || other.status == status)&&(identical(other.version, version) || other.version == version)&&(identical(other.uptimeSeconds, uptimeSeconds) || other.uptimeSeconds == uptimeSeconds)&&(identical(other.serverTimeUtc, serverTimeUtc) || other.serverTimeUtc == serverTimeUtc)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,version,uptimeSeconds,serverTimeUtc,components);

@override
String toString() {
  return 'DiagnosticsReady(status: $status, version: $version, uptimeSeconds: $uptimeSeconds, serverTimeUtc: $serverTimeUtc, components: $components)';
}


}

/// @nodoc
abstract mixin class $DiagnosticsReadyCopyWith<$Res>  {
  factory $DiagnosticsReadyCopyWith(DiagnosticsReady value, $Res Function(DiagnosticsReady) _then) = _$DiagnosticsReadyCopyWithImpl;
@useResult
$Res call({
 String status, String version, int uptimeSeconds, String serverTimeUtc, DiagnosticsReadyComponents components
});


$DiagnosticsReadyComponentsCopyWith<$Res> get components;

}
/// @nodoc
class _$DiagnosticsReadyCopyWithImpl<$Res>
    implements $DiagnosticsReadyCopyWith<$Res> {
  _$DiagnosticsReadyCopyWithImpl(this._self, this._then);

  final DiagnosticsReady _self;
  final $Res Function(DiagnosticsReady) _then;

/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? status = null,Object? version = null,Object? uptimeSeconds = null,Object? serverTimeUtc = null,Object? components = null,}) {
  return _then(_self.copyWith(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,version: null == version ? _self.version : version // ignore: cast_nullable_to_non_nullable
as String,uptimeSeconds: null == uptimeSeconds ? _self.uptimeSeconds : uptimeSeconds // ignore: cast_nullable_to_non_nullable
as int,serverTimeUtc: null == serverTimeUtc ? _self.serverTimeUtc : serverTimeUtc // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as DiagnosticsReadyComponents,
  ));
}
/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$DiagnosticsReadyComponentsCopyWith<$Res> get components {

  return $DiagnosticsReadyComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// Adds pattern-matching-related methods to [DiagnosticsReady].
extension DiagnosticsReadyPatterns on DiagnosticsReady {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DiagnosticsReady value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DiagnosticsReady() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DiagnosticsReady value)  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsReady():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DiagnosticsReady value)?  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsReady() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String status,  String version,  int uptimeSeconds,  String serverTimeUtc,  DiagnosticsReadyComponents components)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DiagnosticsReady() when $default != null:
return $default(_that.status,_that.version,_that.uptimeSeconds,_that.serverTimeUtc,_that.components);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String status,  String version,  int uptimeSeconds,  String serverTimeUtc,  DiagnosticsReadyComponents components)  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsReady():
return $default(_that.status,_that.version,_that.uptimeSeconds,_that.serverTimeUtc,_that.components);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String status,  String version,  int uptimeSeconds,  String serverTimeUtc,  DiagnosticsReadyComponents components)?  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsReady() when $default != null:
return $default(_that.status,_that.version,_that.uptimeSeconds,_that.serverTimeUtc,_that.components);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DiagnosticsReady extends DiagnosticsReady {
  const _DiagnosticsReady({required this.status, required this.version, required this.uptimeSeconds, required this.serverTimeUtc, required this.components}): super._();
  factory _DiagnosticsReady.fromJson(Map<String, dynamic> json) => _$DiagnosticsReadyFromJson(json);

/// No Description
@override final  String status;
/// No Description
@override final  String version;
/// Whole elapsed seconds since the service process started, rounded down.
@override final  int uptimeSeconds;
/// Current UTC server time in RFC 3339 form.
@override final  String serverTimeUtc;
/// Fixed named readiness component states for a ready snapshot.
@override final  DiagnosticsReadyComponents components;

/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DiagnosticsReadyCopyWith<_DiagnosticsReady> get copyWith => __$DiagnosticsReadyCopyWithImpl<_DiagnosticsReady>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DiagnosticsReadyToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DiagnosticsReady&&(identical(other.status, status) || other.status == status)&&(identical(other.version, version) || other.version == version)&&(identical(other.uptimeSeconds, uptimeSeconds) || other.uptimeSeconds == uptimeSeconds)&&(identical(other.serverTimeUtc, serverTimeUtc) || other.serverTimeUtc == serverTimeUtc)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,version,uptimeSeconds,serverTimeUtc,components);

@override
String toString() {
  return 'DiagnosticsReady(status: $status, version: $version, uptimeSeconds: $uptimeSeconds, serverTimeUtc: $serverTimeUtc, components: $components)';
}


}

/// @nodoc
abstract mixin class _$DiagnosticsReadyCopyWith<$Res> implements $DiagnosticsReadyCopyWith<$Res> {
  factory _$DiagnosticsReadyCopyWith(_DiagnosticsReady value, $Res Function(_DiagnosticsReady) _then) = __$DiagnosticsReadyCopyWithImpl;
@override @useResult
$Res call({
 String status, String version, int uptimeSeconds, String serverTimeUtc, DiagnosticsReadyComponents components
});


@override $DiagnosticsReadyComponentsCopyWith<$Res> get components;

}
/// @nodoc
class __$DiagnosticsReadyCopyWithImpl<$Res>
    implements _$DiagnosticsReadyCopyWith<$Res> {
  __$DiagnosticsReadyCopyWithImpl(this._self, this._then);

  final _DiagnosticsReady _self;
  final $Res Function(_DiagnosticsReady) _then;

/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? status = null,Object? version = null,Object? uptimeSeconds = null,Object? serverTimeUtc = null,Object? components = null,}) {
  return _then(_DiagnosticsReady(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,version: null == version ? _self.version : version // ignore: cast_nullable_to_non_nullable
as String,uptimeSeconds: null == uptimeSeconds ? _self.uptimeSeconds : uptimeSeconds // ignore: cast_nullable_to_non_nullable
as int,serverTimeUtc: null == serverTimeUtc ? _self.serverTimeUtc : serverTimeUtc // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as DiagnosticsReadyComponents,
  ));
}

/// Create a copy of DiagnosticsReady
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$DiagnosticsReadyComponentsCopyWith<$Res> get components {

  return $DiagnosticsReadyComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// @nodoc
mixin _$DiagnosticsReadyComponents {

/// No Description
 String get database;/// No Description
 String get schema;
/// Create a copy of DiagnosticsReadyComponents
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DiagnosticsReadyComponentsCopyWith<DiagnosticsReadyComponents> get copyWith => _$DiagnosticsReadyComponentsCopyWithImpl<DiagnosticsReadyComponents>(this as DiagnosticsReadyComponents, _$identity);

  /// Serializes this DiagnosticsReadyComponents to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DiagnosticsReadyComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'DiagnosticsReadyComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class $DiagnosticsReadyComponentsCopyWith<$Res>  {
  factory $DiagnosticsReadyComponentsCopyWith(DiagnosticsReadyComponents value, $Res Function(DiagnosticsReadyComponents) _then) = _$DiagnosticsReadyComponentsCopyWithImpl;
@useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class _$DiagnosticsReadyComponentsCopyWithImpl<$Res>
    implements $DiagnosticsReadyComponentsCopyWith<$Res> {
  _$DiagnosticsReadyComponentsCopyWithImpl(this._self, this._then);

  final DiagnosticsReadyComponents _self;
  final $Res Function(DiagnosticsReadyComponents) _then;

/// Create a copy of DiagnosticsReadyComponents
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_self.copyWith(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [DiagnosticsReadyComponents].
extension DiagnosticsReadyComponentsPatterns on DiagnosticsReadyComponents {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DiagnosticsReadyComponents value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DiagnosticsReadyComponents value)  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DiagnosticsReadyComponents value)?  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String database,  String schema)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String database,  String schema)  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents():
return $default(_that.database,_that.schema);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String database,  String schema)?  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsReadyComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DiagnosticsReadyComponents extends DiagnosticsReadyComponents {
  const _DiagnosticsReadyComponents({required this.database, required this.schema}): super._();
  factory _DiagnosticsReadyComponents.fromJson(Map<String, dynamic> json) => _$DiagnosticsReadyComponentsFromJson(json);

/// No Description
@override final  String database;
/// No Description
@override final  String schema;

/// Create a copy of DiagnosticsReadyComponents
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DiagnosticsReadyComponentsCopyWith<_DiagnosticsReadyComponents> get copyWith => __$DiagnosticsReadyComponentsCopyWithImpl<_DiagnosticsReadyComponents>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DiagnosticsReadyComponentsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DiagnosticsReadyComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'DiagnosticsReadyComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class _$DiagnosticsReadyComponentsCopyWith<$Res> implements $DiagnosticsReadyComponentsCopyWith<$Res> {
  factory _$DiagnosticsReadyComponentsCopyWith(_DiagnosticsReadyComponents value, $Res Function(_DiagnosticsReadyComponents) _then) = __$DiagnosticsReadyComponentsCopyWithImpl;
@override @useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class __$DiagnosticsReadyComponentsCopyWithImpl<$Res>
    implements _$DiagnosticsReadyComponentsCopyWith<$Res> {
  __$DiagnosticsReadyComponentsCopyWithImpl(this._self, this._then);

  final _DiagnosticsReadyComponents _self;
  final $Res Function(_DiagnosticsReadyComponents) _then;

/// Create a copy of DiagnosticsReadyComponents
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_DiagnosticsReadyComponents(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$DiagnosticsUnavailable {

/// No Description
 String get status;/// Fixed named readiness component states without an unavailable cause.
 DiagnosticsUnavailableComponents get components;
/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DiagnosticsUnavailableCopyWith<DiagnosticsUnavailable> get copyWith => _$DiagnosticsUnavailableCopyWithImpl<DiagnosticsUnavailable>(this as DiagnosticsUnavailable, _$identity);

  /// Serializes this DiagnosticsUnavailable to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DiagnosticsUnavailable&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'DiagnosticsUnavailable(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class $DiagnosticsUnavailableCopyWith<$Res>  {
  factory $DiagnosticsUnavailableCopyWith(DiagnosticsUnavailable value, $Res Function(DiagnosticsUnavailable) _then) = _$DiagnosticsUnavailableCopyWithImpl;
@useResult
$Res call({
 String status, DiagnosticsUnavailableComponents components
});


$DiagnosticsUnavailableComponentsCopyWith<$Res> get components;

}
/// @nodoc
class _$DiagnosticsUnavailableCopyWithImpl<$Res>
    implements $DiagnosticsUnavailableCopyWith<$Res> {
  _$DiagnosticsUnavailableCopyWithImpl(this._self, this._then);

  final DiagnosticsUnavailable _self;
  final $Res Function(DiagnosticsUnavailable) _then;

/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? status = null,Object? components = null,}) {
  return _then(_self.copyWith(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as DiagnosticsUnavailableComponents,
  ));
}
/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$DiagnosticsUnavailableComponentsCopyWith<$Res> get components {

  return $DiagnosticsUnavailableComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// Adds pattern-matching-related methods to [DiagnosticsUnavailable].
extension DiagnosticsUnavailablePatterns on DiagnosticsUnavailable {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DiagnosticsUnavailable value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailable() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DiagnosticsUnavailable value)  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailable():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DiagnosticsUnavailable value)?  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailable() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String status,  DiagnosticsUnavailableComponents components)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailable() when $default != null:
return $default(_that.status,_that.components);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String status,  DiagnosticsUnavailableComponents components)  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailable():
return $default(_that.status,_that.components);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String status,  DiagnosticsUnavailableComponents components)?  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailable() when $default != null:
return $default(_that.status,_that.components);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DiagnosticsUnavailable extends DiagnosticsUnavailable {
  const _DiagnosticsUnavailable({required this.status, required this.components}): super._();
  factory _DiagnosticsUnavailable.fromJson(Map<String, dynamic> json) => _$DiagnosticsUnavailableFromJson(json);

/// No Description
@override final  String status;
/// Fixed named readiness component states without an unavailable cause.
@override final  DiagnosticsUnavailableComponents components;

/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DiagnosticsUnavailableCopyWith<_DiagnosticsUnavailable> get copyWith => __$DiagnosticsUnavailableCopyWithImpl<_DiagnosticsUnavailable>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DiagnosticsUnavailableToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DiagnosticsUnavailable&&(identical(other.status, status) || other.status == status)&&(identical(other.components, components) || other.components == components));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,status,components);

@override
String toString() {
  return 'DiagnosticsUnavailable(status: $status, components: $components)';
}


}

/// @nodoc
abstract mixin class _$DiagnosticsUnavailableCopyWith<$Res> implements $DiagnosticsUnavailableCopyWith<$Res> {
  factory _$DiagnosticsUnavailableCopyWith(_DiagnosticsUnavailable value, $Res Function(_DiagnosticsUnavailable) _then) = __$DiagnosticsUnavailableCopyWithImpl;
@override @useResult
$Res call({
 String status, DiagnosticsUnavailableComponents components
});


@override $DiagnosticsUnavailableComponentsCopyWith<$Res> get components;

}
/// @nodoc
class __$DiagnosticsUnavailableCopyWithImpl<$Res>
    implements _$DiagnosticsUnavailableCopyWith<$Res> {
  __$DiagnosticsUnavailableCopyWithImpl(this._self, this._then);

  final _DiagnosticsUnavailable _self;
  final $Res Function(_DiagnosticsUnavailable) _then;

/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? status = null,Object? components = null,}) {
  return _then(_DiagnosticsUnavailable(
status: null == status ? _self.status : status // ignore: cast_nullable_to_non_nullable
as String,components: null == components ? _self.components : components // ignore: cast_nullable_to_non_nullable
as DiagnosticsUnavailableComponents,
  ));
}

/// Create a copy of DiagnosticsUnavailable
/// with the given fields replaced by the non-null parameter values.
@override
@pragma('vm:prefer-inline')
$DiagnosticsUnavailableComponentsCopyWith<$Res> get components {

  return $DiagnosticsUnavailableComponentsCopyWith<$Res>(_self.components, (value) {
    return _then(_self.copyWith(components: value));
  });
}
}


/// @nodoc
mixin _$DiagnosticsUnavailableComponents {

/// No Description
 String get database;/// No Description
 String get schema;
/// Create a copy of DiagnosticsUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$DiagnosticsUnavailableComponentsCopyWith<DiagnosticsUnavailableComponents> get copyWith => _$DiagnosticsUnavailableComponentsCopyWithImpl<DiagnosticsUnavailableComponents>(this as DiagnosticsUnavailableComponents, _$identity);

  /// Serializes this DiagnosticsUnavailableComponents to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is DiagnosticsUnavailableComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'DiagnosticsUnavailableComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class $DiagnosticsUnavailableComponentsCopyWith<$Res>  {
  factory $DiagnosticsUnavailableComponentsCopyWith(DiagnosticsUnavailableComponents value, $Res Function(DiagnosticsUnavailableComponents) _then) = _$DiagnosticsUnavailableComponentsCopyWithImpl;
@useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class _$DiagnosticsUnavailableComponentsCopyWithImpl<$Res>
    implements $DiagnosticsUnavailableComponentsCopyWith<$Res> {
  _$DiagnosticsUnavailableComponentsCopyWithImpl(this._self, this._then);

  final DiagnosticsUnavailableComponents _self;
  final $Res Function(DiagnosticsUnavailableComponents) _then;

/// Create a copy of DiagnosticsUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_self.copyWith(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [DiagnosticsUnavailableComponents].
extension DiagnosticsUnavailableComponentsPatterns on DiagnosticsUnavailableComponents {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _DiagnosticsUnavailableComponents value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _DiagnosticsUnavailableComponents value)  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _DiagnosticsUnavailableComponents value)?  $default,){
final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String database,  String schema)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String database,  String schema)  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents():
return $default(_that.database,_that.schema);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String database,  String schema)?  $default,) {final _that = this;
switch (_that) {
case _DiagnosticsUnavailableComponents() when $default != null:
return $default(_that.database,_that.schema);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _DiagnosticsUnavailableComponents extends DiagnosticsUnavailableComponents {
  const _DiagnosticsUnavailableComponents({required this.database, required this.schema}): super._();
  factory _DiagnosticsUnavailableComponents.fromJson(Map<String, dynamic> json) => _$DiagnosticsUnavailableComponentsFromJson(json);

/// No Description
@override final  String database;
/// No Description
@override final  String schema;

/// Create a copy of DiagnosticsUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$DiagnosticsUnavailableComponentsCopyWith<_DiagnosticsUnavailableComponents> get copyWith => __$DiagnosticsUnavailableComponentsCopyWithImpl<_DiagnosticsUnavailableComponents>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$DiagnosticsUnavailableComponentsToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _DiagnosticsUnavailableComponents&&(identical(other.database, database) || other.database == database)&&(identical(other.schema, schema) || other.schema == schema));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,database,schema);

@override
String toString() {
  return 'DiagnosticsUnavailableComponents(database: $database, schema: $schema)';
}


}

/// @nodoc
abstract mixin class _$DiagnosticsUnavailableComponentsCopyWith<$Res> implements $DiagnosticsUnavailableComponentsCopyWith<$Res> {
  factory _$DiagnosticsUnavailableComponentsCopyWith(_DiagnosticsUnavailableComponents value, $Res Function(_DiagnosticsUnavailableComponents) _then) = __$DiagnosticsUnavailableComponentsCopyWithImpl;
@override @useResult
$Res call({
 String database, String schema
});




}
/// @nodoc
class __$DiagnosticsUnavailableComponentsCopyWithImpl<$Res>
    implements _$DiagnosticsUnavailableComponentsCopyWith<$Res> {
  __$DiagnosticsUnavailableComponentsCopyWithImpl(this._self, this._then);

  final _DiagnosticsUnavailableComponents _self;
  final $Res Function(_DiagnosticsUnavailableComponents) _then;

/// Create a copy of DiagnosticsUnavailableComponents
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? database = null,Object? schema = null,}) {
  return _then(_DiagnosticsUnavailableComponents(
database: null == database ? _self.database : database // ignore: cast_nullable_to_non_nullable
as String,schema: null == schema ? _self.schema : schema // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}


/// @nodoc
mixin _$Error {

/// Non-empty human-readable error message.
 String get error;
/// Create a copy of Error
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ErrorCopyWith<Error> get copyWith => _$ErrorCopyWithImpl<Error>(this as Error, _$identity);

  /// Serializes this Error to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Error&&(identical(other.error, error) || other.error == error));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,error);

@override
String toString() {
  return 'Error(error: $error)';
}


}

/// @nodoc
abstract mixin class $ErrorCopyWith<$Res>  {
  factory $ErrorCopyWith(Error value, $Res Function(Error) _then) = _$ErrorCopyWithImpl;
@useResult
$Res call({
 String error
});




}
/// @nodoc
class _$ErrorCopyWithImpl<$Res>
    implements $ErrorCopyWith<$Res> {
  _$ErrorCopyWithImpl(this._self, this._then);

  final Error _self;
  final $Res Function(Error) _then;

/// Create a copy of Error
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? error = null,}) {
  return _then(_self.copyWith(
error: null == error ? _self.error : error // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [Error].
extension ErrorPatterns on Error {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _Error value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _Error() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _Error value)  $default,){
final _that = this;
switch (_that) {
case _Error():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _Error value)?  $default,){
final _that = this;
switch (_that) {
case _Error() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String error)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _Error() when $default != null:
return $default(_that.error);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String error)  $default,) {final _that = this;
switch (_that) {
case _Error():
return $default(_that.error);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String error)?  $default,) {final _that = this;
switch (_that) {
case _Error() when $default != null:
return $default(_that.error);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _Error extends Error {
  const _Error({required this.error}): super._();
  factory _Error.fromJson(Map<String, dynamic> json) => _$ErrorFromJson(json);

/// Non-empty human-readable error message.
@override final  String error;

/// Create a copy of Error
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ErrorCopyWith<_Error> get copyWith => __$ErrorCopyWithImpl<_Error>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ErrorToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _Error&&(identical(other.error, error) || other.error == error));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,error);

@override
String toString() {
  return 'Error(error: $error)';
}


}

/// @nodoc
abstract mixin class _$ErrorCopyWith<$Res> implements $ErrorCopyWith<$Res> {
  factory _$ErrorCopyWith(_Error value, $Res Function(_Error) _then) = __$ErrorCopyWithImpl;
@override @useResult
$Res call({
 String error
});




}
/// @nodoc
class __$ErrorCopyWithImpl<$Res>
    implements _$ErrorCopyWith<$Res> {
  __$ErrorCopyWithImpl(this._self, this._then);

  final _Error _self;
  final $Res Function(_Error) _then;

/// Create a copy of Error
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? error = null,}) {
  return _then(_Error(
error: null == error ? _self.error : error // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
