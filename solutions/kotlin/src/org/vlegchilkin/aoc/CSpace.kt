package org.vlegchilkin.aoc

import kotlin.math.abs

typealias C = Pair<Int, Int>

data class CSpace<T>(val n: Int, val m: Int, val data: MutableMap<C, T>) {
  operator fun get(c: C): T? = data[c]
  fun links(pos: C, directions: List<Direction> = Direction.all(), hasPath: ((C) -> Boolean)? = null): List<C> {
    val pathChecker = hasPath ?: { it in data }
    return directions.map { pos + it }.filter { pathChecker(it) }
  }

  override fun toString(): String {
    return buildString {
      for (i in 0..<n) {
        for (j in 0..<m) {
          append(data[i to j] ?: '.')
        }
        append('\n')
      }
    }
  }
}

fun <T> String.toCSpace(mapper: (Char) -> T?): CSpace<T> {
  val array = this.toList { it }
  val n = array.size
  val m = if (n > 0) array[0].length else 0
  val data = mutableMapOf<C, T>().apply {
    array.forEachIndexed { i, line ->
      line.forEachIndexed { j, value ->
        mapper(value)?.let { put(i to j, it) }
      }
    }
  }
  return CSpace(n, m, data)
}

enum class Direction(val vector: C, vararg val aliases: Char) {
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
    fun ofVector(vector: C) = Direction.entries.find { it.vector == vector }
    fun of(direction: Char) = Direction.entries.find { direction in it.aliases }
  }
}


fun <T> List<T>.toPair(): Pair<T, T> {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun List<Int>.toC(): C {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun Collection<C>.area(): Pair<C, C> {
  val low = this.minOf { it.first } to this.minOf { it.second }
  val high = this.maxOf { it.first } to this.maxOf { it.second }
  return low to high
}

fun C.clockwise() = this.second to -this.first
operator fun C.times(steps: Int) = this.first * steps to this.second * steps
operator fun C.unaryMinus(): C = -this.first to -this.second
operator fun C.plus(direction: Direction): C = this + direction.vector
operator fun C.plus(other: C): C = (this.first + other.first) to (this.second + other.second)
operator fun C.minus(other: C): C = (this.first - other.first) to (this.second - other.second)
operator fun C.rangeTo(max: C) = this to max
operator fun Pair<C, C>.contains(x: C): Boolean {
  return x.first in this.first.first..this.second.first &&
         x.second in this.first.second..this.second.second
}

infix fun C.manhattanTo(other: C): Int {
  return abs(this.first - other.first) + abs(this.second - other.second)
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