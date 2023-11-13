package org.vlegchilkin.aoc

import com.google.common.collect.Sets

fun <T> Collection<T>.combinations(size: Int) = sequence {
  val s: Set<T> = toSet()
  for (x in Sets.combinations(s, size)) {
    yield(x.toList())
  }
}

fun Boolean.toInt() = if (this) 1 else 0