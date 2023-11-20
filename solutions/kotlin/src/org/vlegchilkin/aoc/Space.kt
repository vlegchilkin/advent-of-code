package org.vlegchilkin.aoc

import kotlin.math.abs

enum class Direction(val vector: Pair<Int, Int>, vararg val aliases: Char) {
  N(-1 to 0, '^', 'N'),
  NE(-1 to 1),
  E(0 to 1, '>', 'E'),
  SE(1 to 1),
  S(1 to 0, 'v', 'S'),
  SW(1 to -1),
  W(0 to -1, '<', 'W'),
  NW(-1 to -1);

  fun turn(action: Char): Direction {
    return when (action) {
      'F' -> this
      'B' -> -this
      'R' -> ofVector(this.vector.clockwise())!!
      'L' -> ofVector(-this.vector.clockwise())!!
      else -> throw IllegalArgumentException("Not supported action: $action")
    }
  }

  operator fun unaryMinus(): Direction = ofVector(-this.vector.first to -this.vector.second)!!
  operator fun times(steps: Int) = vector * steps
  operator fun plus(coordinate: Pair<Int, Int>) = this.vector + coordinate


  companion object {
    fun diagonals() = listOf(NE, SE, SW, NW)
    fun borders() = listOf(N, E, S, W)
    fun all(): List<Direction> = Direction.entries
    fun ofVector(vector: Pair<Int, Int>) = Direction.entries.find { it.vector == vector }
    fun of(direction: Char) = Direction.entries.find { direction in it.aliases }
  }
}

fun <T> List<T>.toPair(): Pair<T, T> {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun Collection<Pair<Int, Int>>.area(): Pair<Pair<Int, Int>, Pair<Int, Int>> {
  return (this.minOf { it.first } to this.minOf { it.second }) to (this.maxOf { it.first } to this.maxOf { it.second })
}

fun Pair<Int, Int>.clockwise() = this.second to -this.first
operator fun Pair<Int, Int>.times(steps: Int) = this.first * steps to this.second * steps
operator fun Pair<Int, Int>.unaryMinus(): Pair<Int, Int> = -this.first to -this.second
operator fun Pair<Int, Int>.plus(direction: Direction): Pair<Int, Int> = this + direction.vector
operator fun Pair<Int, Int>.plus(other: Pair<Int, Int>): Pair<Int, Int> = (this.first + other.first) to (this.second + other.second)
operator fun Pair<Int, Int>.rangeTo(max: Pair<Int, Int>) = this to max
operator fun Pair<Pair<Int, Int>, Pair<Int, Int>>.contains(x: Pair<Int, Int>): Boolean {
  return x.first in this.first.first..this.second.first &&
         x.second in this.first.second..this.second.second
}

infix fun Pair<Int, Int>.manhattanTo(other: Pair<Int, Int>): Int {
  return abs(this.first - other.first) + abs(this.second - other.second)
}


fun wrap3D(pos: Triple<Int, Int, Int>): List<Triple<Int, Int, Int>> {
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


fun transform(form: Array<IntArray>, func: (Array<IntArray>, Int, Int) -> Int): Array<IntArray> {
  val m = form.size
  val res = Array(m) { IntArray(m) { 0 } }
  for (i in 0..<m) {
    for (j in 0..<m) {
      res[i][j] = func(form, i, j)
    }
  }
  return res
}

fun clockwise(form: Array<IntArray>): Array<IntArray> {
  return transform(form) { f, i, j -> f[f.size - j - 1][i] }
}

fun flip(form: Array<IntArray>): Array<IntArray> {
  return transform(form) { f, i, j -> form[i][f.size - j - 1] }
}

fun translate(form: Array<IntArray>): List<Array<IntArray>> {
  val result = mutableListOf<Array<IntArray>>()
  var base = form
  repeat(2) {
    result.add(base)
    repeat(3) {
      base = clockwise(base).also { result.add(it) }
    }
    base = flip(base)
  }
  return result
}