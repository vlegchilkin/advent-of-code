package org.vlegchilkin.aoc

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

