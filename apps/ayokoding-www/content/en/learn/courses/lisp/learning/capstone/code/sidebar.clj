;; Clojure sidebar: defmacro is explicit about generated bindings.
(defmacro unless* [condition & body]
  `(if (not ~condition) (do ~@body) nil))

(defn sum-positive [values]
  (reduce (fn [total value] (if (pos? value) (+ total value) total)) 0 values))

(println (sum-positive [4 -2 6]))
(unless* false (println "macro body ran"))
