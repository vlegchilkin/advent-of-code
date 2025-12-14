package org.vlegchilkin.aoc

import kotlin.collections.contains
import kotlin.collections.set

typealias Graph<T> = Map<T, Collection<T>>

fun <T> Graph<T>.topologicalSort(nodes: Collection<T>): List<T> {
  val remains = nodes.toMutableSet()
  val reverseOrdered = mutableListOf<T>()

  fun dfs(nodes: Collection<T>) {
    nodes.forEach { node ->
      if (!remains.remove(node)) return@forEach
      this[node]?.let { dfs(it) }
      reverseOrdered.add(node)
    }
  }

  dfs(nodes)

  return reverseOrdered.asReversed()
}

fun <T> Graph<T>.topologicalTransitiveSort(nodes: Collection<T>): List<T> {
  return topologicalSort(keys).filter { nodes.contains(it) }
}

fun <T> Graph<T>.components(): List<Set<T>> {
  val result = mutableListOf<Set<T>>()
  val unprocessed = this.keys.toMutableSet()
  while (unprocessed.isNotEmpty()) {
    val start = unprocessed.first().also { unprocessed.remove(it) }
    val pack = mutableSetOf<T>()
    val queue = ArrayDeque(listOf(start))
    while (queue.isNotEmpty()) {
      val node = queue.removeFirst()
      pack.add(node)
      this[node]?.forEach {
        if (unprocessed.remove(it)) queue.add(it)
      }
    }
    result.add(pack)
  }
  return result
}