package org.vlegchilkin.aoc

import com.google.common.collect.Sets

fun <T> Collection<T>.combinations(size: Int) = sequence {
  val s: Set<T> = toSet()
  for (x in Sets.combinations(s, size)) {
    yield(x.toList())
  }
}

fun Boolean.toInt() = if (this) 1 else 0

fun <R> String.toList(delimiter: String = "\n",
                      conv: (String) -> R) = this.trim().split(delimiter).filter { it.isNotBlank() }.map { conv(it) }

fun <R> String.toListIndexed(delimiter: String = "\n",
                             conv: (Int, String) -> R) = this.trim().split(delimiter).filter { it.isNotBlank() }.mapIndexed { i, v -> conv(i, v) }

fun String.toIntList(filter: Regex = """\d+""".toRegex()) = filter.findAll(this).map { it.value.toInt() }.toList()
