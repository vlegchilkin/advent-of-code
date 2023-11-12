package org.vlegchilkin.aoc

import com.google.common.collect.Sets

interface Solution {
  fun runA(): Any = ""
  fun runB(): Any = ""
  fun runAB(): Pair<Any, Any> = runA() to runB()
}

fun <T> Collection<T>.combinations(size: Int) = sequence {
  val s: Set<T> = toSet()
  for (x in Sets.combinations(s, size)) {
    yield(x.toList())
  }
}