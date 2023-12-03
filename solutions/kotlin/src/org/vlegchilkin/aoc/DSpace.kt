package org.vlegchilkin.aoc

import kotlin.math.abs

typealias D = Triple<Int, Int, Int>

data class DSpace<T>(val n: Int, val m: Int, val k: Int, val data: MutableMap<D, T>) {
  operator fun get(d: D): T? = data[d]
}

fun List<Int>.toD(): D {
  if (this.size != 3) {
    throw IllegalArgumentException("List is not of length 3!")
  }
  return Triple(this[0], this[1], this[2])
}

fun Collection<D>.area(): Pair<D, D> {
  val low = Triple(this.minOf { it.first }, this.minOf { it.second }, this.minOf { it.third })
  val high = Triple(this.maxOf { it.first }, this.maxOf { it.second }, this.maxOf { it.third })
  return low to high
}

operator fun Pair<D, D>.contains(x: D): Boolean {
  return x.first in this.first.first..this.second.first &&
         x.second in this.first.second..this.second.second &&
         x.third in this.first.third..this.second.third
}

infix fun D.manhattanTo(other: D): Int {
  return abs(this.first - other.first) + abs(this.second - other.second) + abs(this.third - other.third)
}

fun wrap3D(pos: D): List<D> {
  return (pos.first - 1..pos.first + 1).map { x ->
    (pos.second - 1..pos.second + 1).map { y ->
      (pos.third - 1..pos.third + 1).filter { pos.first != x || pos.second != y || pos.third != it }.map { z ->
        Triple(x, y, z)
      }
    }.flatten()
  }.flatten()
}

fun wrapMultiD(pos: List<Int>): List<List<Int>> {
  if (pos.isEmpty()) return listOf(listOf())
  val res = wrapMultiD(pos.drop(1))
  return (pos[0] - 1..pos[0] + 1).flatMap { c0 -> res.map { cInner -> listOf(c0) + cInner } }
}
