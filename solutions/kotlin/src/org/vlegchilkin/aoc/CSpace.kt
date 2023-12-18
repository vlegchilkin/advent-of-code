package org.vlegchilkin.aoc

import kotlin.math.abs

typealias C = Pair<Int, Int>

data class CSpace<T : Any>(var rows: IntRange, var cols: IntRange, val data: MutableMap<C, T>) : MutableMap<C, T> {
  override operator fun get(key: C): T? = data[key]
  override val size: Int
    get() = data.size
  override val entries: MutableSet<MutableMap.MutableEntry<C, T>>
    get() = data.entries
  override val keys: MutableSet<C>
    get() = data.keys
  override val values: MutableCollection<T>
    get() = data.values

  override fun clear() {
    data.clear()
  }

  val rowsCount: Int
    get() = rows.last - rows.first + 1
  val colsCount: Int
    get() = cols.last - cols.first + 1

  override fun put(key: C, value: T) = data.put(key, value)

  override fun putAll(from: Map<out C, T>) = data.putAll(from)

  override fun remove(key: C) = data.remove(key)

  override fun containsKey(key: C) = data.containsKey(key)

  override fun containsValue(value: T) = data.containsValue(value)

  override fun isEmpty() = data.isEmpty()

  fun links(pos: C, directions: List<Direction> = Direction.all(), hasPath: ((C) -> Boolean)? = null): List<C> {
    val pathChecker = hasPath ?: { isBelongs(it) }
    return directions.map { pos + it }.filter { pathChecker(it) }
  }

  override fun toString(): String {
    return buildString {
      for (i in rows) {
        for (j in cols) {
          append(data[i to j] ?: '.')
        }
        append('\n')
      }
    }
  }

  fun expand(border: Int): CSpace<T> {
    val r = this.rows.first - border..this.rows.last + border
    val c = this.cols.first - border..this.cols.last + border
    return CSpace(r, c, data.toMutableMap())
  }

  fun clone(): CSpace<T> {
    return expand(0)
  }

  fun <R : Any> transform(conv: (C, T?) -> R?): CSpace<R> {
    val newData = mutableMapOf<C, R>()
    view().forEach { (pos, value) -> conv(pos, value)?.let { newData[pos] = it } }
    return CSpace(rows, cols, newData)
  }

  fun fill(start: C, value: (C) -> T) {
    val queue = ArrayDeque<C>()
    queue.addLast(start)
    while (queue.isNotEmpty()) {
      val pos = queue.removeFirst()
      links(pos, directions = Direction.borders()) { isBelongs(it) && it !in data }.forEach {
        data[it] = value(it)
        queue.addLast(it)
      }
    }
  }

  fun isBelongs(pos: C) = pos.first in rows && pos.second in cols

  fun isEmpty(pos: C) = isBelongs(pos) && pos !in this

  fun view(): Sequence<Pair<C, T?>> = sequence {
    for (row in rows) {
      for (col in cols) {
        val pos = row to col
        yield(pos to data[pos])
      }
    }
  }
}

fun <T : Any> String.toCSpace(mapper: (Char) -> T?): CSpace<T> {
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
  return CSpace(0..<n, 0..<m, data)
}

enum class Side {
  F, B, R, L;

  companion object {
    fun of(char: Char): Side {
      return Side.valueOf("$char")
    }

    fun Char.toSide(): Side {
      return of(this)
    }
  }
}

enum class Direction(val vector: C, vararg val aliases: Char) {
  N(-1 to 0, '^', 'N', 'U'),
  NE(-1 to 1),
  E(0 to 1, '>', 'E', 'R'),
  SE(1 to 1),
  S(1 to 0, 'v', 'S', 'D'),
  SW(1 to -1),
  W(0 to -1, '<', 'W', 'L'),
  NW(-1 to -1);

  infix fun turn(side: Side): Direction {
    return when (side) {
      Side.F -> this
      Side.B -> -this
      Side.R -> ofVector(this.vector.clockwise())!!
      Side.L -> ofVector(-this.vector.clockwise())!!
    }
  }

  operator fun unaryMinus(): Direction = ofVector(-this.vector.first to -this.vector.second)!!
  operator fun times(steps: Int) = vector * steps
  operator fun plus(coordinate: C) = this.vector + coordinate


  companion object {
    fun diagonals() = listOf(NE, SE, SW, NW)
    fun borders() = listOf(N, E, S, W)
    fun all(): List<Direction> = Direction.entries
    fun ofVector(vector: C) = Direction.entries.find { it.vector == vector }
    fun of(direction: Char) = Direction.entries.find { direction in it.aliases }
  }
}

fun List<Int>.toC(): C {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun Collection<C>.minmax(): Pair<C, C> {
  val low = this.minOf { it.first } to this.minOf { it.second }
  val high = this.maxOf { it.first } to this.maxOf { it.second }
  return low to high
}

fun Collection<C>.area(): Long {
  val polygon = this.map { it.first.toLong() to it.second.toLong() }
  var area = 0L
  var j = polygon.indices.last
  for (i in polygon.indices) {
    area += (polygon[j].first + polygon[i].first) * (polygon[j].second - polygon[i].second)
    j = i
  }
  return abs(area / 2)
}
fun Collection<C>.path(): Long {
  return this.windowed(2).fold(0L) { acc, (a, b) ->
    acc + abs(a.first - b.first) + abs(a.second - b.second)
  }
}

fun C.clockwise() = this.second to -this.first
operator fun C.times(steps: Int) = this.first * steps to this.second * steps
operator fun C.unaryMinus(): C = -this.first to -this.second
operator fun C.plus(direction: Direction): C = this + direction.vector
operator fun C.minus(direction: Direction): C = this - direction.vector
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