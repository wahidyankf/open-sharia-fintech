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
