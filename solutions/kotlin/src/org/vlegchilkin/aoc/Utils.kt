package org.vlegchilkin.aoc

import com.google.common.collect.Sets
import kotlin.reflect.KClass

fun <T> Collection<T>.combinations(size: Int) = sequence {
  val s: Set<T> = toSet()
  for (x in Sets.combinations(s, size)) {
    yield(x.toList())
  }
}

fun <T> List<T>.toPair(): Pair<T, T> {
  if (this.size != 2) {
    throw IllegalArgumentException("List is not of length 2!")
  }
  return Pair(this[0], this[1])
}

fun <T> List<T>.toTriple(): Triple<T, T, T> {
  if (this.size != 3) {
    throw IllegalArgumentException("List is not of length 3!")
  }
  return Triple(this[0], this[1], this[2])
}


fun Boolean.toInt() = if (this) 1 else 0
fun Pair<String, String>.toLong() = this.first.toLong() to this.second.toLong()

fun <T : Any> List<String>.toObject(clazz: KClass<T>): T {
  val constructor = clazz.constructors.first { it.parameters.size == this.size }
  val args = constructor.parameters.zip(this).map { (param, value) ->
    when (param.type.toString()) {
      "kotlin.Int" -> value.toInt()
      "kotlin.Long" -> value.toLong()
      "kotlin.String" -> value
      else -> throw UnsupportedOperationException("${param.type} is not supported")
    }
  }.toTypedArray()
  return constructor.call(*args)
}

fun <R> String.toList(delimiter: String = "\n",
                      conv: (String) -> R) = this.trim().split(delimiter).filter { it.isNotBlank() }.map { conv(it) }

fun <R> String.toListIndexed(delimiter: String = "\n",
                             conv: (Int, String) -> R) = this.trim().split(delimiter).filter { it.isNotBlank() }.mapIndexed { i, v -> conv(i, v) }

fun String.toIntList(filter: Regex = """\d+""".toRegex()) = filter.findAll(this).map { it.value.toInt() }.toList()
fun String.toLongList(filter: Regex = """\d+""".toRegex()) = filter.findAll(this).map { it.value.toLong() }.toList()
