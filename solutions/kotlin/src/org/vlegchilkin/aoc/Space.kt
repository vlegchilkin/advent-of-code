package org.vlegchilkin.aoc

enum class Direction(val vector: Pair<Int, Int>) {
  NORTH(-1 to 0),
  NORTH_EAST(-1 to 1),
  EAST(0 to 1),
  SOUTH_EAST(1 to 1),
  SOUTH(1 to 0),
  SOUTH_WEST(1 to -1),
  WEST(0 to -1),
  NORTH_WEST(-1 to -1);

  companion object {
    fun diagonals() = listOf(NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST)
    fun borders() = listOf(NORTH, SOUTH, WEST, EAST)
    fun all(): List<Direction> = Direction.entries
  }
}

fun <T> List<T>.toPair(): Pair<T, T> {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun Collection<Pair<Int, Int>>.area(): Pair<Pair<Int, Int>, Pair<Int, Int>>  {
  return (this.minOf { it.first } to this.minOf { it.second }) to (this.maxOf { it.first } to this.maxOf { it.second })
}

operator fun Direction.plus(coordinate: Pair<Int, Int>): Pair<Int, Int> = this.vector + coordinate
operator fun Pair<Int, Int>.plus(direction: Direction): Pair<Int, Int> = this + direction.vector
operator fun Pair<Int, Int>.plus(other: Pair<Int, Int>): Pair<Int, Int> = (this.first + other.first) to (this.second + other.second)
operator fun Pair<Int, Int>.rangeTo(max: Pair<Int, Int>) = this to max
operator fun Pair<Pair<Int, Int>, Pair<Int, Int>>.contains(x: Pair<Int, Int>): Boolean {
  return x.first in this.first.first..this.second.first &&
         x.second in this.first.second..this.second.second
}

